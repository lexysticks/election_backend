from django.apps import AppConfig


class VoteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vote'
from django.apps import AppConfig

class ElectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vote'  # Replace with your app name

    def ready(self):
        import vote.signals  # Registers signals automatically
