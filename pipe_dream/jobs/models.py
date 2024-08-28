from django.db import models
from django.utils import timezone

class RepoCredentials(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name
    # implement using JSON field
    # https://pypi.org/project/django-json-field/

class Repo(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    credentials = models.ForeignKey(RepoCredentials, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class DeployDestination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # implement using JSON field

    def __str__(self) -> str:
        return self.name

class Job(models.Model):
    name = models.CharField(max_length=50, unique = True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    # script = models.FileField()
    schedule = models.TimeField() # index on this
    deployTo = models.ManyToManyField(to=DeployDestination)

    def __str__(self) -> str:
        return self.name + " " + str(self.schedule)

class Run(models.Model):
    class RunState(models.TextChoices):
        SCHEDULED = 'S'
        RUNNING = 'O'
        COMPLETE = 'C'
        FAILED = 'F'

    id = models.BigAutoField(primary_key=True) #explicit PK to use for scheduling
    job = models.ForeignKey(Job, 
                            on_delete=models.CASCADE, 
                            related_name="runs")
    number = models.IntegerField() #not unique on its own, only per Job
    buildStatus = models.CharField(max_length=1,
                                   choices=RunState.choices,
                                   default=RunState.SCHEDULED)
    scheduled = models.DateTimeField(default=timezone.now)
    started = models.DateTimeField(blank=True, null=True)
    completed = models.DateTimeField(blank=True, null=True)
    
    # store output as a JSON object, may contain paths to files with script stdout/stderr
    
    def __str__(self) -> str:
        return self.job.name + ' #' + str(self.number)
    
    class Meta:
        get_latest_by = 'started'

class Scheduling(models.Model):
    lastSuccessful = models.DateTimeField(default=timezone.now)