# https://django-background-tasks.readthedocs.io/en/latest/

# should probably use Celery, beyond the scope of this assignment
# for the purposes of this demo, run this as if it were on `cron`

from jobs.runner import Scheduler, Runner

def doRun(runId: int):
    Runner.go(runId)

Scheduler.checkAndScheduleRuns(doRun)
