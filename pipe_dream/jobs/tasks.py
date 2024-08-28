# https://django-background-tasks.readthedocs.io/en/latest/

# should probably use Celery, better community support, but that would require
# Redis or RabbitMQ, which is beyond the scope of this assignment

from background_task import background
from .models import Run
from .runner import Scheduler, Runner

@background()
def check_schedule():
    Scheduler.checkAndScheduleRuns(doRun)

@background()
def doRun(runId: int):
    Runner.go(runId)
