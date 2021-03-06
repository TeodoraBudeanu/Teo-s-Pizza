from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, unique=True)


@receiver(post_save, sender=User)
def create_user_account(sender, instance, **kwargs):
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        Account.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_account(sender, instance, **kwargs):
    if not kwargs.get('raw', False):
        instance.account.save()
