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

    def test_scheduled_run_time_used_to_evaluate_downtime(self):
        """
        the latest that a task was scheduled should be used as the last time the scheduler ran
        """
        latest = Run.objects.latest().scheduled
        self.assertEqual(latest, self.run.scheduled)

    def test_scheduler_calls_do_run(self):
        """
        scheduler should schedule the job with the callback
        """

        results = RunnerTests.Results()
        Scheduler.checkAndScheduleRuns(results.doRun)

        self.assertTrue(results.didRun)

    def test_only_one_scheduler_at_a_time(self):
        """
        if a scheduler is already running, cancel the scheduler run
        """
        from background_task.models import Task
        Task.objects.create(task_name='jobs.tasks.check_schedule',
                            run_at=timezone.now())

        results = RunnerTests.Results()
        Scheduler.checkAndScheduleRuns(results.doRun)

        self.assertFalse(results.didRun)