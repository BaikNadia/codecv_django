from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class CVProfile(models.Model):
    """Профиль резюме пользователя"""

    # Выбор темы
    THEME_CHOICES = [
        ("github-dark", "GitHub Dark"),
        ("github-light", "GitHub Light"),
        ("dracula", "Dracula"),
        ("nord", "Nord"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="cv_profile"
    )
    slug = models.SlugField(unique=True, blank=True)

    # Основная информация
    github_username = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    bio = models.TextField(blank=True)
    headline = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Настройки
    theme = models.CharField(
        max_length=20, choices=THEME_CHOICES, default="github-dark"
    )
    github_data = models.JSONField(default=dict, blank=True)  # Кэш данных GitHub
    is_public = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профиль резюме"
        verbose_name_plural = "Профили резюме"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Автоматическое создание slug при сохранении"""
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            while CVProfile.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Резюме: {self.user.username}"


class Skill(models.Model):
    """Навык пользователя"""

    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("tools", "Tools & DevOps"),
        ("mobile", "Mobile"),
        ("soft", "Soft Skills"),
    ]

    profile = models.ForeignKey(
        CVProfile, on_delete=models.CASCADE, related_name="skills"
    )
    name = models.CharField(max_length=100)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="tools"
    )
    level = models.IntegerField(default=3, choices=[(i, str(i)) for i in range(1, 6)])
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["order", "-level", "name"]
        unique_together = ["profile", "name"]  # Один навык на профиль

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"


class Project(models.Model):
    """Проект пользователя (из GitHub или ручной ввод)"""

    profile = models.ForeignKey(
        CVProfile, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies = models.CharField(max_length=500, blank=True)  # Разделенные запятыми
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(upload_to="projects/", blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["order", "-is_featured", "-created_at"]

    def __str__(self):
        return self.title


# from django.db import models
# from django.contrib.auth.models import User
#
# class CVProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cv_profile")
#     github_username = models.CharField(max_length=100, blank=True)
#     bio = models.TextField(blank=True)
#
#     def __str__(self):
#         return f"CV: {self.user.username}"
#
# class Skill(models.Model):
#     profile = models.ForeignKey(CVProfile, on_delete=models.CASCADE, related_name="skills")
#     name = models.CharField(max_length=100)
#     level = models.IntegerField(default=3, choices=[(i, str(i)) for i in range(1, 6)])
#
#     def __str__(self):
#         return self.name
