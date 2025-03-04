from django.db import models 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response  
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
class CountUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)                               
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name', 'username']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        permissions = [('can_view_count_user', 'Can view count user')]

    # Définition des related_name pour groups et user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='count_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='count_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class UserPlant(models.Model):
    plant_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(CountUser, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=255)
    image = models.ImageField(default='default.jpg', upload_to='images/')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = 'User Plant'
        verbose_name_plural = 'User Plants'

    def __str__(self):
        return f"Plante {self.name} (Utilisateur: {self.user.email})"
