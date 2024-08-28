from django.apps import AppConfig

class JobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "jobs"

    def ready(self):
        # not ideal to do this in app start, could do an endpoint instead?
        from .tasks import check_schedule
        check_schedule(repeat=5)
