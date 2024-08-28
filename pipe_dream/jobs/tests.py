from django.test import TransactionTestCase

from datetime import time

from .models import Run, Job, DeployDestination, Repo, RepoCredentials
from .runner import Scheduler

class RunnerTests(TransactionTestCase):
    def setUp(self):
        repoCredentials = RepoCredentials(name="mock cred")
        repoCredentials.save()
        
        repo = Repo(name="mock repo", 
                    url="http://ghi.fds", 
                    credentials=repoCredentials)
        repo.save()
        dest = DeployDestination(name="mock dest")
        dest.save()
        job = Job(name="mock job",
                repo=repo,
                schedule=time(0,0))
        job.save()
        job.deployTo.add(dest)
        job.save()
        
        run = Run(job=job,
                buildStatus = Run.RunState.SCHEDULED,
                number=1)
        run.save()

    def test_scheduled_run_time_used_to_test_for_downtime(self):
        """
        the latest that a task was scheduled should be used as the last time the scheduler ran
        """
        latest = Run.objects.latest().scheduled
        self.assertEqual(latest, self.run)
