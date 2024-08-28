from .models import Job, Run, Repo, Scheduling
from typing import Callable
from django.utils import timezone
from datetime import datetime, time, timedelta

class Scheduler:
    def checkAndScheduleRuns(doRun: Callable[[Run], None]):
        now = timezone.now()
        today = now.date()
        yesterday = now + timedelta(days=-1)
        beginningOfToday = datetime.combine(today, time(0))

        try:
            scheduling = Scheduling.objects.only()
        except Scheduling.DoesNotExist:
            scheduling = Scheduling.objects.create(lastSuccessful=beginningOfToday)

        lastRunTimestamp = scheduling.lastSuccessful
        if lastRunTimestamp < yesterday:
            lastRunTimestamp = beginningOfToday

        # if last scheduled task was within the past 24 hours,
        #  maybe there are missed tasks from before 00:00
        if lastRunTimestamp < beginningOfToday:
            jobsToSchedule = Job.objects.filter(
                schedule__range=(lastRunTimestamp.time, time(23,59,59))
            ) | Job.objects.filter(
                schedule__range=(time(0,0), now.time)
            )
        else:
            jobsToSchedule = Job.objects.filter(
                schedule__range=(lastRunTimestamp.time, now.time)
            )

        for job in jobsToSchedule:
            run = Runner.createRun(job)
            doRun(run) 

        scheduling.lastSuccessful = timezone.now()
        scheduling.save()       

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

