from django.contrib import admin
from .models import Job, RepoCredentials, Repo, DeployDestination, Run

admin.site.register((Job, RepoCredentials, Repo, DeployDestination, Run))