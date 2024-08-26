from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

class RepoCredentials(models.Model):
    name = models.TextField(unique=True)
    # implement using JSON field
    # https://pypi.org/project/django-json-field/

class Repo(models.Model):
    name = models.TextField(unique=True)
    url = models.URLField()
    credentials = models.ForeignKey(RepoCredentials, on_delete=models.CASCADE)

class DeployDestination(models.Model):
    name = models.TextField(unique=True)
    # implement using JSON field

class Job(models.Model):
    name = models.TextField(unique = True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    # script = models.FileField()

class Run(models.Model):
    number = models.IntegerField(unique=True)
    # buildStatus = 

    # class CompletionState(models.TextChoices):
    #     NEW = 'N', _('New')
    #     OPEN = 'O', _('Open')
    #     DONE = 'D', _('Done')
    #     ARCHIVED = 'A', _('Archived')

    # title = models.CharField(max_length=50)
    # description = models.TextField()
    # priority = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(10)])
    # state=models.CharField(max_length=1,
    #                        choices=CompletionState.choices,
    #                        default=CompletionState.NEW)
    # surprise=models.BooleanField(default=False)
