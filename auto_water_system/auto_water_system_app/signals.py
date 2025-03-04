from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CountUser

@receiver(post_save, sender=CountUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Crée automatiquement un profil pour chaque nouvel utilisateur.
    """
    if created:
       CountUser.objects.create(username=instance.username)

@receiver(post_save, sender=CountUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Sauvegarde automatiquement le profil lorsque l'utilisateur est mis à jour.
    """
    instance.profile.save()
