import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from rest_framework import serializers

from .models import CVProfile, Skill


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]
        read_only_fields = ["id", "username"]


class SkillSerializer(serializers.ModelSerializer):
    category_display = serializers.CharField(
        source="get_category_display", read_only=True
    )

    class Meta:
        model = Skill
        fields = [
            "id",
            "name",
            "category",
            "category_display",
            "level",
            "order",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate_level(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Уровень навыка должен быть от 1 до 5")
        return value

    def create(self, validated_data):
        """Создание навыка с привязкой к профилю пользователя"""
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            profile, created = CVProfile.objects.get_or_create(user=request.user)
            validated_data["profile"] = profile
            return super().create(validated_data)
        raise serializers.ValidationError("Требуется авторизация")


class GitHubRepoSerializer(serializers.Serializer):
    """Сериализатор для репозиториев GitHub"""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(
        read_only=True, allow_blank=True, allow_null=True
    )
    html_url = serializers.URLField(read_only=True)
    language = serializers.CharField(read_only=True, allow_null=True)
    stargazers_count = serializers.IntegerField(read_only=True)
    forks_count = serializers.IntegerField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CVProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    # Вычисляемые поля
    skills_count = serializers.SerializerMethodField()
    github_repos = serializers.SerializerMethodField()
    github_languages = serializers.SerializerMethodField()

    class Meta:
        model = CVProfile
        fields = [
            "id",
            "user",
            "username",
            "email",
            "github_username",
            "bio",
            "headline",
            "location",
            "website",
            "avatar",
            "theme",
            "is_public",
            "views",
            "skills",
            "skills_count",
            "github_data",
            "github_repos",
            "github_languages",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "username",
            "email",
            "views",
            "created_at",
            "updated_at",
            "github_data",
        ]

    def get_skills_count(self, obj):
        return obj.skills.count()

    def get_github_repos(self, obj):
        if obj.github_data and "repos" in obj.github_data:
            repos = obj.github_data.get("repos", [])[:6]
            return GitHubRepoSerializer(repos, many=True).data
        return []

    def get_github_languages(self, obj):
        if obj.github_data and "languages" in obj.github_data:
            languages = obj.github_data.get("languages", {})
            sorted_languages = dict(
                sorted(languages.items(), key=lambda x: x[1], reverse=True)[:8]
            )
            return [
                {"name": lang, "count": count}
                for lang, count in sorted_languages.items()
            ]
        return []

    def validate_github_username(self, value):
        if not value:
            return value

        # Простая проверка существования пользователя
        try:
            response = requests.get(f"https://api.github.com/users/{value}", timeout=5)
            if response.status_code == 404:
                raise serializers.ValidationError("Пользователь GitHub не найден")
        except requests.exceptions.RequestException:
            # Если нет интернета, пропускаем проверку
            pass

        return value

    def update(self, instance, validated_data):
        github_username = validated_data.get("github_username")

        # Если изменился github_username, очищаем старые данные
        if github_username and github_username != instance.github_username:
            instance.github_data = {}
            instance.github_username = github_username

            # Удаляем старые навыки из GitHub
            instance.skills.filter(
                models.Q(category="backend") | models.Q(category="frontend")
            ).delete()

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            if attr != "github_username":
                setattr(instance, attr, value)

        instance.save()
        return instance


class GitHubSyncSerializer(serializers.Serializer):
    """Сериализатор для синхронизации с GitHub"""

    force = serializers.BooleanField(default=False, required=False)

    def validate(self, attrs):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Требуется авторизация")
        return attrs

    def save(self, profile):
        from .github_integration import GitHubAPI

        force = self.validated_data.get("force", False)

        # Проверяем, нужна ли синхронизация
        if not force and profile.github_data:
            last_sync = profile.github_data.get("synced_at")
            if last_sync:
                from dateutil.parser import parse

                last_sync_time = parse(last_sync)
                if (timezone.now() - last_sync_time).seconds < 3600:
                    return {
                        "status": "skipped",
                        "reason": "Синхронизировано менее часа назад",
                    }

        try:
            github = GitHubAPI()
            user_data = github.get_user_data(profile.github_username)
            repos = github.get_user_repos(profile.github_username, limit=10)
            languages = github.analyze_languages(repos)

            profile.github_data = {
                "user": user_data,
                "repos": repos[:6],
                "languages": languages,
                "synced_at": timezone.now().isoformat(),
            }
            profile.save(update_fields=["github_data"])

            # Создаем навыки из языков
            self.create_skills_from_languages(profile, languages)

            return {
                "status": "success",
                "repos_synced": len(repos),
                "languages_found": len(languages),
            }

        except Exception as e:
            raise serializers.ValidationError(str(e))

    def create_skills_from_languages(self, profile, languages):
        from .models import Skill

        backend_langs = {
            "Python",
            "Java",
            "C++",
            "C#",
            "Go",
            "Rust",
            "PHP",
            "Ruby",
            "Scala",
            "Kotlin",
        }
        frontend_langs = {
            "JavaScript",
            "TypeScript",
            "HTML",
            "CSS",
            "Sass",
            "Less",
            "Vue",
            "React",
        }
        mobile_langs = {"Swift", "Kotlin", "Dart", "Objective-C"}

        for lang, count in languages.items():
            if lang in backend_langs:
                category = "backend"
            elif lang in frontend_langs:
                category = "frontend"
            elif lang in mobile_langs:
                category = "mobile"
            else:
                category = "tools"

            if count >= 5:
                level = 5
            elif count >= 3:
                level = 4
            elif count >= 2:
                level = 3
            else:
                level = 2

            Skill.objects.update_or_create(
                profile=profile,
                name=lang,
                defaults={"category": category, "level": level, "order": 100 - count},
            )
