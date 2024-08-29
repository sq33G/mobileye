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

class NotifyDestination(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # implement using JSON field

    def __str__(self) -> str:
        return self.name

class ActionAssociation(models.TextChoices):
    PRELOAD = 'L'
    PREBUILD = 'B'
    PREDEPLOY = 'D'
    PRENOTIFY = 'N'
    ONCOMPLETE = 'O'

class Job(models.Model):
    name = models.CharField(max_length=50, unique = True)
    repo = models.ForeignKey(Repo, on_delete=models.CASCADE)
    # script = models.FileField()
    schedule = models.TimeField() # index on this
    deployTo = models.ManyToManyField(to=DeployDestination)
    notifyTo = models.ManyToManyField(to=NotifyDestination, blank=True)

    def __str__(self) -> str:
        return self.name + " " + str(self.schedule)
    
    def preload_actions(self):
        return self.actionsByAssociation(ActionAssociation.PRELOAD)
    
    def prebuild_actions(self):
        return self.actionsByAssociation(ActionAssociation.PREBUILD)
    
    def predeploy_actions(self):
        return self.actionsByAssociation(ActionAssociation.PREDEPLOY)
    
    def prenotify_actions(self):
        return self.actionsByAssociation(ActionAssociation.PRENOTIFY)
    
    def oncomplete_actions(self):
        return self.actionsByAssociation(ActionAssociation.ONCOMPLETE)
    
    def actionsByAssociation(self, association:ActionAssociation):
        return self.actions.filter(association = association)

class Action(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # script = models.FileField
    job = models.ForeignKey(Job, 
                            on_delete=models.CASCADE,
                            related_name="actions")
    association = models.CharField(max_length=1,
                                   choices=ActionAssociation.choices,
                                   default=ActionAssociation.PREBUILD)
    
    def __str__(self):
        return self.name + " (" + self.association + ", " + self.job + ")"

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
    
    def start(self):
        self.started = timezone.now()
        self.buildStatus = Run.RunState.RUNNING
        self.save()

    def complete(self):
        self.completed = timezone.now()
        self.buildStatus = Run.RunState.COMPLETE
        self.save()

    # should record whether success or failure...
    
    class Meta:
        get_latest_by = 'started'

class Scheduling(models.Model):
    lastSuccessful = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return "Last successful run at " + str(self.lastSuccessful)