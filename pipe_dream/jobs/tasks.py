# https://django-background-tasks.readthedocs.io/en/latest/

from background_task import background
from .models import Run
from .runner import Scheduler, Runner

@background()
def check_schedule():
    Scheduler.checkAndScheduleRuns(doRun)

@background()
def doRun(run: Run):
    Runner.go(run)
