from django.db import models

class RepoCredentials(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # implement using JSON field
    # https://pypi.org/project/django-json-field/

class Repo(models.Model):
    name = models.CharField(max_length=50, unique=True)
    url = models.URLField()
    credentials = models.ForeignKey(RepoCredentials, on_delete=models.CASCADE)

class DeployDestination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # implement using JSON field

class Job(models.Model):
    name = models.CharField(max_length=50, unique = True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    # script = models.FileField()

class Run(models.Model):
    class RunState(models.TextChoices):
        SCHEDULED = 'S'
        RUNNING = 'O'
        COMPLETE = 'C'
        FAILED = 'F'

    number = models.IntegerField() #not unique on its own, only per Job
    buildStatus = models.CharField(max_length=1,
                                   choices=RunState.choices,
                                   default=RunState.SCHEDULED)
    
    # store output as a JSON object, may contain paths to files with script stdout/stderr
    