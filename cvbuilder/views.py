# from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse
# from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.core.files.storage import FileSystemStorage
import os

from .github_integration import GitHubAPI
from .models import CVProfile, Skill
from .serializers import CVProfileSerializer, GitHubSyncSerializer, SkillSerializer


# ==================== Django View Functions ====================


def cv_detail(request, username):
    """Публичная страница резюме"""
    profile = get_object_or_404(CVProfile, user__username=username, is_public=True)

    # Увеличиваем счетчик просмотров
    profile.views += 1
    profile.save(update_fields=["views"])

    context = {
        "profile": profile,
        "skills": profile.skills.all(),
        "is_owner": request.user == profile.user,
    }

    return render(request, "cvbuilder/cv_detail.html", context)


@login_required
def cv_edit(request):
    """Редактирование резюме"""
    profile, created = CVProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Обработка формы
        profile.github_username = request.POST.get('github_username', '')
        profile.bio = request.POST.get('bio', '')
        profile.headline = request.POST.get('headline', '')
        profile.location = request.POST.get('location', '')
        profile.website = request.POST.get('website', '')
        profile.theme = request.POST.get('theme', 'github-dark')
        profile.is_public = request.POST.get('is_public') == 'true'

        # Обработка аватара
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            # Проверка размера файла
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                messages.error(request, 'Файл слишком большой. Максимальный размер: 2MB')
            else:
                # Сохраняем файл
                profile.avatar = avatar
                messages.success(request, 'Аватар успешно загружен')

        # Удаление аватара
        if request.POST.get('avatar-clear'):
            if profile.avatar:
                # Удаляем файл с диска
                if os.path.isfile(profile.avatar.path):
                    os.remove(profile.avatar.path)
                profile.avatar.delete(save=False)
                profile.avatar = None
                messages.success(request, 'Аватар удален')

        try:
            profile.save()
            messages.success(request, 'Профиль успешно сохранен')
            return redirect('cv_detail', username=request.user.username)
        except Exception as e:
            messages.error(request, f'Ошибка сохранения: {str(e)}')

    return render(request, 'cvbuilder/cv_edit.html', {'profile': profile})


@login_required
def sync_github(request):
    """Синхронизация с GitHub (для HTMX/традиционных views)"""
    try:
        profile = request.user.cv_profile
    except CVProfile.DoesNotExist:
        profile = CVProfile.objects.create(user=request.user)

    if not profile.github_username:
        return JsonResponse({"error": "GitHub username not set"}, status=400)

    try:
        github = GitHubAPI()
        user_data = github.get_user_data(profile.github_username)
        repos = github.get_user_repos(profile.github_username, limit=10)
        languages = github.analyze_languages(repos)

        # Сохраняем данные
        profile.github_data = {
            "user": user_data,
            "repos": repos[:6],
            "languages": languages,
            "synced_at": timezone.now().isoformat(),
        }
        profile.save()

        # Создаем навыки из языков программирования
        for lang, count in languages.items():
            Skill.objects.get_or_create(
                profile=profile,
                name=lang,
                defaults={
                    "category": (
                        "backend" if lang in ["Python", "Java", "Go"] else "frontend"
                    )
                },
            )

        return JsonResponse({"success": True, "data": profile.github_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ==================== Django REST Framework Views ====================


class CVProfileViewSet(viewsets.ModelViewSet):
    """ViewSet для API профилей"""

    queryset = CVProfile.objects.all()
    serializer_class = CVProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Публичные профили или свои
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return CVProfile.objects.all()
            return CVProfile.objects.filter(
                models.Q(is_public=True) | models.Q(user=self.request.user)
            )
        return CVProfile.objects.filter(is_public=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def sync_github(self, request, pk=None):
        profile = self.get_object()

        # Проверка прав
        if profile.user != request.user and not request.user.is_staff:
            return Response(
                {"error": "Нет прав для синхронизации этого профиля"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = GitHubSyncSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            try:
                result = serializer.save(profile)
                return Response(result)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def my_profile(self, request):
        """Получение профиля текущего пользователя"""
        if not request.user.is_authenticated:
            return Response(
                {"error": "Требуется авторизация"}, status=status.HTTP_401_UNAUTHORIZED
            )

        profile, created = CVProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class SkillViewSet(viewsets.ModelViewSet):
    """ViewSet для API навыков"""

    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = CVProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


# ==================== API Views ====================


class PublicProfileAPI(APIView):
    """API для получения публичного профиля"""

    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        try:
            profile = CVProfile.objects.get(user__username=username, is_public=True)

            # Увеличиваем счетчик просмотров
            profile.views += 1
            profile.save(update_fields=["views"])

            serializer = CVProfileSerializer(profile)
            return Response(serializer.data)

        except CVProfile.DoesNotExist:
            return Response(
                {"error": "Профиль не найден или не является публичным"},
                status=status.HTTP_404_NOT_FOUND,
            )
