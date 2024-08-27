from .models import Job, Run, Repo
from typing import Callable
from django.utils import timezone
from datetime import datetime, time

class Scheduler:
    def checkAndScheduleRuns(doRun: Callable[[Run], None]):
        now = timezone.now()
        today = now.date()
        beginningOfToday = datetime.combine(today, time(0))

        try:
            lastRunTimestamp = Run.objects.latest().started
        except Run.DoesNotExist:
            lastRunTimestamp = beginningOfToday

        if lastRunTimestamp.date() < today:
            lastRunTimestamp = beginningOfToday

        # use prefetch to make this more efficient
        jobsToSchedule = Job.objects.filter(
            schedule__range=(lastRunTimestamp.time(),
                             now.time()))
        for job in jobsToSchedule:
            run = Runner.createRun(job)
            doRun(run)        

class Runner:
    def createRun(job: Job) -> Run:
        try:
            newJobRunNumber = Run.objects.filter(job=job).latest().number + 1
        except Run.DoesNotExist:
            newJobRunNumber = 1
            
        # if it's still running, probably delay this... or cancel it??
        # also consider if two runs for the same job might get scheduled concurrently??
        run = Run(job = job, 
                buildStatus = Run.RunState.SCHEDULED,
                number = newJobRunNumber)
        run.save()

        return run
    
    def go(run: Run):
        run.start()
        # set working directory to unique for job...
        Runner.load(run.job.repo)
        run.begin_build()
        Runner.build(run)
        run.begin_deploy()
        Runner.deploy(run)
        run.begin_notify()
        Runner.notify(run)
        # in future, allow more actions...
        run.complete()
    
    def load(repo: Repo):
        print('mock: cloning ', repo)

    def build(run: Run):
        print('mock: building ', run)

    def deploy(run: Run):
        for dest in run.job.deployTo:
            print('mock: deploy results from ', run, ' to ', dest)

    def notify(run: Run):
        print('not implemented: notify')

