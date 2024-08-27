from .models import Job, Run, Repo
from typing import Callable
from django.utils import timezone
from datetime import timedelta

class Scheduler:
    def checkAndScheduleRuns(doRun: Callable[[Run], None]):
        try:
            lastRunTimestamp = Run.objects.latest().started
        except Run.DoesNotExist:
            lastRunTimestamp = timezone.now() + timedelta(days=-1)

        # use prefetch to make this more efficient
        jobsToSchedule = Job.objects.filter(
            schedule__range=(lastRunTimestamp.time(),
                             timezone.now().time()))
        for job in jobsToSchedule:
            run = Runner.createRun(job)
            doRun(run)        

class Runner:
    def createRun(job: Job) -> Run:
        newJobRunNumber = Run.objects.filter(job=job).latest().number + 1
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

