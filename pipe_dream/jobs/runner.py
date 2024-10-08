from .models import Job, Run, Repo, Scheduling, Action
from typing import Callable, List
from django.utils import timezone
from datetime import datetime, time, timedelta

class Scheduler:
    def checkAndScheduleRuns(doRun: Callable[[Run], None]):
        now = timezone.now()
        today = now.date()
        yesterday = now + timedelta(days=-1)
        beginningOfToday = datetime.combine(today, time(0, tzinfo=timezone.get_current_timezone()))

        lastRunTimestamp = None

        try:
            scheduling = Scheduling.objects.get()
            lastRunTimestamp = scheduling.lastSuccessful
        except Scheduling.DoesNotExist:
            # if somehow the scheduler starts running again while this scheduler is
            # in progress, we will have a race condition that will lead to there being
            # more than one row in Scheduling. Some kind of locking would help.
            scheduling = Scheduling.objects.create(lastSuccessful=beginningOfToday)

        if not lastRunTimestamp or (lastRunTimestamp < yesterday):
            lastRunTimestamp = beginningOfToday

        # if last scheduled task was within the past 24 hours,
        #  maybe there are missed tasks from before 00:00
        if lastRunTimestamp < beginningOfToday:
            jobsToSchedule = Job.objects.filter(
                schedule__range=(lastRunTimestamp.time(), time(23,59,59))
            ) | Job.objects.filter(
                schedule__range=(time(0,0), now.time())
            )
        else:
            jobsToSchedule = Job.objects.filter(
                schedule__range=(lastRunTimestamp.time(), now.time())
            )

        runs = []
        for job in jobsToSchedule:
            run = Runner.createRun(job)
            runs.append(run)
        
        # this could be split out to run on different machines to manage load

        for run in runs:
            doRun(run.id) 

        scheduling.lastSuccessful = now + timedelta(seconds=1)
        scheduling.save()       

class Runner:
    def createRun(job: Job) -> Run:
        #test if job is already scheduled, don't schedule if so - need to know how to look at task args for this
        # alreadyRunning = Scheduler.checkAlreadyRunning("jobs.tasks.check_schedule")
        # if alreadyRunning:
        #     print('scheduler already running, cancel')
        #     return

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
    
    def go(runId: int):
        run = Run.objects.filter(id=runId).get()
        run.start()
        # set working directory to unique for job...
        Runner.runActions(run.job.preload_actions())
        Runner.load(run.job.repo)
        Runner.runActions(run.job.prebuild_actions())
        Runner.build(run)
        Runner.runActions(run.job.predeploy_actions())
        Runner.deploy(run)
        Runner.runActions(run.job.prenotify_actions())
        Runner.notify(run)
        Runner.runActions(run.job.oncomplete_actions())
        run.complete()
    
    def load(repo: Repo):
        print('mock: cloning ', repo)

    def build(run: Run):
        print('mock: building ', run)

    def deploy(run: Run):
        for dest in run.job.deployTo.all():
            print('mock: deploy results from ', run, ' to ', dest)

    def notify(run: Run):
        for dest in run.job.notifyTo.all():
            print('mock: notify of results from ', run, ' to ', dest)

    def runActions(actions: List[Action]):
        for action in actions:
            print('mock: run action ', action)


