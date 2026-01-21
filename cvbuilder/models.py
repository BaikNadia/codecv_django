from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
import os


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
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    # Основная информация
    github_username = models.CharField(max_length=100, blank=True)

    # Аватар с валидацией
    avatar = models.ImageField(
        upload_to="avatars/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])
        ],
        help_text="Поддерживаемые форматы: JPG, PNG, GIF, WebP. Максимальный размер: 2MB"
    )

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
        """Автоматическое создание slug и обработка аватара при сохранении"""

        # Генерация slug
        if not self.slug:
            base_slug = slugify(self.user.username)
            slug = base_slug
            counter = 1
            while CVProfile.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Удаление старого аватара при замене
        if self.pk:
            try:
                old_instance = CVProfile.objects.get(pk=self.pk)
                if old_instance.avatar and old_instance.avatar != self.avatar:
                    # Удаляем старый файл с диска
                    if os.path.isfile(old_instance.avatar.path):
                        os.remove(old_instance.avatar.path)
            except CVProfile.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаление аватара при удалении профиля"""
        if self.avatar:
            if os.path.isfile(self.avatar.path):
                os.remove(self.avatar.path)
        super().delete(*args, **kwargs)

    def get_avatar_url(self):
        """Безопасное получение URL аватара"""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return None

    def get_initials(self):
        """Получение инициалов для отображения при отсутствии аватара"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        return self.user.username[:2].upper()

    def __str__(self):
        return f"Резюме: {self.user.username}"

    @property
    def display_name(self):
        """Отображаемое имя пользователя"""
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username


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
    name = models.CharField(max_length=100, db_index=True)
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="tools", db_index=True
    )
    level = models.IntegerField(
        default=3,
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text="Уровень от 1 (новичок) до 5 (эксперт)"
    )
    order = models.IntegerField(default=0, help_text="Порядок отображения")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["order", "-level", "name"]
        unique_together = ["profile", "name"]  # Один навык на профиль

    def get_level_display(self):
        """Текстовое представление уровня"""
        level_names = {
            1: "Новичок",
            2: "Начальный",
            3: "Средний",
            4: "Продвинутый",
            5: "Эксперт"
        }
        return level_names.get(self.level, str(self.level))

    def get_progress_width(self):
        """Ширина прогресс-бара в процентах"""
        return self.level * 20  # 1=20%, 2=40%, 3=60%, 4=80%, 5=100%

    def __str__(self):
        return f"{self.name} - {self.get_level_display()}"


class Project(models.Model):
    """Проект пользователя (из GitHub или ручной ввод)"""

    profile = models.ForeignKey(
        CVProfile, on_delete=models.CASCADE, related_name="projects"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    technologies = models.CharField(
        max_length=500,
        blank=True,
        help_text="Технологии, разделенные запятыми"
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)

    # Изображение проекта с валидацией
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'webp'])
        ],
        help_text="Изображение проекта. Максимальный размер: 5MB"
    )

    is_featured = models.BooleanField(default=False, db_index=True)
    order = models.IntegerField(default=0, help_text="Порядок отображения")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["order", "-is_featured", "-created_at"]

    def save(self, *args, **kwargs):
        """Удаление старого изображения при замене"""
        if self.pk:
            try:
                old_instance = Project.objects.get(pk=self.pk)
                if old_instance.image and old_instance.image != self.image:
                    if os.path.isfile(old_instance.image.path):
                        os.remove(old_instance.image.path)
            except Project.DoesNotExist:
                pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаление изображения при удалении проекта"""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)

    def get_technologies_list(self):
        """Получение списка технологий"""
        if self.technologies:
            return [tech.strip() for tech in self.technologies.split(",")]
        return []

    def __str__(self):
        return self.title


# Сигналы для дополнительной обработки (опционально)
from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender=CVProfile)
def delete_cvprofile_files(sender, instance, **kwargs):
    """Удаление файлов при удалении профиля"""
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)


@receiver(pre_delete, sender=Project)
def delete_project_files(sender, instance, **kwargs):
    """Удаление файлов при удалении проекта"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
