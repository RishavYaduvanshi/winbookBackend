from django.dispatch import receiver
from . import models
from django.db.models.signals import m2m_changed, pre_save
from django.conf import settings
from django.apps import apps

User = apps.get_model(settings.AUTH_USER_MODEL)

