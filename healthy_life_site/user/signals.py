from django.contrib.auth.signals import user_logged_in, user_logged_out
from pharmacy.models import LoyaltyCard
from user.models import User, Settings
from django.db.models.signals import post_save, post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver


@receiver(user_logged_in)
def set_user_online(sender, request, user, **kwargs):
    user.is_online = True
    user.save()


@receiver(user_logged_out)
def set_user_offline(sender, request, user, **kwargs):
    user.is_online = False
    user.save()


@receiver(post_migrate)
def create_base_roles_if_not_exists(sender, **kwargs):
    Group.objects.get_or_create(name='Модератор')
    Group.objects.get_or_create(name='Курьер')
    Group.objects.get_or_create(name='Фармацевт')


@receiver(post_save, sender=User)
def create_user_related_models(sender, instance, created, **kwargs):
    if created:
        Settings.objects.create(user_settings=instance)
        LoyaltyCard.objects.create(user_card=instance)
