from django.test import TestCase

from datetime import time
from django.utils import timezone

from .models import Run, Job, DeployDestination, Repo, RepoCredentials
from .runner import Scheduler

class RunnerTests(TestCase):
    class Results:
        didRun = False

        def doRun(self, run):
            self.didRun = True

    def setUp(self):
        self.repoCredentials = RepoCredentials(name="mock cred")
        self.repoCredentials.save()
        
        self.repo = Repo(name="mock repo", 
                    url="http://ghi.fds", 
                    credentials=self.repoCredentials)
        self.repo.save()
        self.dest = DeployDestination(name="mock dest")
        self.dest.save()
        self.job = Job(name="mock job",
                repo=self.repo,
                schedule=timezone.now().time())
        self.job.save()
        self.job.deployTo.add(self.dest)
        self.job.save()
        
        self.run = Run(job=self.job,
                buildStatus = Run.RunState.SCHEDULED,
                number=1)
        self.run.save()

    def test_scheduler_calls_do_run(self):
        """
        scheduler should schedule the job with the callback
        """

        results = RunnerTests.Results()
        Scheduler.checkAndScheduleRuns(results.doRun)

        self.assertTrue(results.didRun)

    # add tests to check different cases of last scheduler run : now