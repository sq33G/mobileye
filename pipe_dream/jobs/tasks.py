# https://django-background-tasks.readthedocs.io/en/latest/

from background_task import background
from .models import Job, Run

@background()
def check_schedule(user_id):
    