
from django.contrib import admin
from .models import CVProfile, Skill

@admin.register(CVProfile)
class CVProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "github_username")

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "profile", "level")
