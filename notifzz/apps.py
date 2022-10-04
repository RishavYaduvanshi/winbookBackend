from django.apps import AppConfig


class NotifzzConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "notifzz"

    def ready(self) -> None:
        from . import signals
