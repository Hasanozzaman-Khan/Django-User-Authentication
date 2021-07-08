from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProfileModel, CustomRegisterModel


@receiver(post_save, sender=CustomRegisterModel)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)


@receiver(post_save, sender=CustomRegisterModel)
def save_profile(sender, instance, **kwargs):
    instance.profilemodel.save()    # profilemodel in lowercase
