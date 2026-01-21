from django.contrib import admin

from .models import CVProfile, Project, Skill


@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "github_username",
        "headline",
        "views",
        "is_public",
        "created_at",
    )
    list_filter = ("is_public", "theme", "created_at")
    search_fields = ("user__username", "github_username", "headline", "bio")
    readonly_fields = ("views", "created_at", "updated_at")
    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "user",
                    "slug",
                    "github_username",
                    "avatar",
                    "headline",
                    "bio",
                )
            },
        ),
        ("Контактная информация", {"fields": ("location", "website")}),
        ("Настройки", {"fields": ("theme", "is_public", "github_data")}),
        ("Статистика", {"fields": ("views", "created_at", "updated_at")}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "profile", "category", "level", "order")
    list_filter = ("category", "level", "created_at")
    search_fields = ("name", "profile__user__username")
    list_editable = ("order", "level")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "is_featured", "created_at")
    list_filter = ("is_featured", "created_at")
    search_fields = ("title", "description", "technologies")
    list_editable = ("is_featured",)
