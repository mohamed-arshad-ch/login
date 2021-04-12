from django.apps import AppConfig


class RegisteruserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registeruser'




    def ready(self):
        import registeruser.signals