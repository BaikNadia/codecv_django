
from django.db import models
from django.contrib.auth.models import User

class CVProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cv_profile")
    github_username = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"CV: {self.user.username}"

class Skill(models.Model):
    profile = models.ForeignKey(CVProfile, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=3, choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self):
        return self.name
