from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Email als Hauptfeld
    USERNAME_FIELD = 'email'  # Django soll E-Mail statt Username verwenden
    REQUIRED_FIELDS = ['username']  # `username` bleibt Pflichtfeld, aber Login per Email

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",  # 🔥 Namenskonflikt lösen
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions_set",  # 🔥 Namenskonflikt lösen
        blank=True
    )

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # WICHTIG: `CustomUser` statt `User`
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
