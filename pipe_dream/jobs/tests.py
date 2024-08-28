from django.test import TestCase

from datetime import time

from .models import Run, Job, DeployDestination, Repo, RepoCredentials
from .runner import Scheduler

class RunnerTests(TestCase):
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
                schedule=time(0,0))
        self.job.save()
        self.job.deployTo.add(self.dest)
        self.job.save()
        
        self.run = Run(job=self.job,
                buildStatus = Run.RunState.SCHEDULED,
                number=1)
        self.run.save()

    def test_scheduled_run_time_used_to_evaluate_downtime(self):
        """
        the latest that a task was scheduled should be used as the last time the scheduler ran
        """
        latest = Run.objects.latest().scheduled
        self.assertEqual(latest, self.run.scheduled)
