from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from cvbuilder.views import CVProfileViewSet, PublicProfileAPI, SkillViewSet

# Создаем router для DRF
router = DefaultRouter()
router.register(r"profiles", CVProfileViewSet, basename="profile")
router.register(r"skills", SkillViewSet, basename="skill")

urlpatterns = [
    # API endpoints (DRF)
    path("", include(router.urls)),
    # Аутентификация
    path("auth/token/", obtain_auth_token, name="api_token_auth"),
    # Публичный профиль
    path(
        "public/profile/<str:username>/",
        PublicProfileAPI.as_view(),
        name="public_profile_api",
    ),
    # Профиль текущего пользователя
    path(
        "my-profile/",
        CVProfileViewSet.as_view({"get": "my_profile"}),
        name="my_profile",
    ),
]
