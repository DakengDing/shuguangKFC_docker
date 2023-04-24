from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Fc

@receiver(post_save, sender=User)
def add_user_fc(sender, instance, created, **kwargs):
    if created:
        Fc.objects.create(user_name=instance, fc=False)