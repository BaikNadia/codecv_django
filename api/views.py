from django.db import models
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cvbuilder.models import CVProfile, Skill
from cvbuilder.serializers import CVProfileSerializer, SkillSerializer


class CVProfileViewSet(viewsets.ModelViewSet):
    queryset = CVProfile.objects.all()
    serializer_class = CVProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Публичные профили или свои
        if self.request.user.is_authenticated:
            return CVProfile.objects.filter(
                models.Q(is_public=True) | models.Q(user=self.request.user)  # ← Теперь models определен
            )
        return CVProfile.objects.filter(is_public=True)

    @action(detail=True, methods=["post"])
    def sync_github(self, request, pk=None):
        profile = self.get_object()
        # Логика синхронизации с GitHub
        # TODO: Добавить реальную логику синхронизации
        # Например:
        # github_data = sync_with_github(profile.github_username)
        # profile.github_data = github_data
        # profile.save()

        return Response({"status": "synced", "profile_id": profile.id})  # ← Используем переменную


class SkillViewSet(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Skill.objects.filter(profile__user=self.request.user)

    def perform_create(self, serializer):
        profile, created = CVProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)
