from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from cvbuilder import views as cv_views


def home(request):
    """Перенаправление на главную страницу"""
    # Если пользователь авторизован - на его профиль, иначе на демо
    if request.user.is_authenticated:
        return redirect("cv_detail", username=request.user.username)
    return redirect("admin:index")  # Или на демо страницу


urlpatterns = [
    path("admin/", admin.site.urls),
    # API
    path("api/", include("api.urls")),
    # Стандартные страницы
    path("cv/<str:username>/", cv_views.cv_detail, name="cv_detail"),
    path("edit/", cv_views.cv_edit, name="cv_edit"),
    path("sync-github/", cv_views.sync_github, name="sync_github"),
    # Главная страница
    path("", home, name="home"),
]

# Для обслуживания медиа файлов в development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
