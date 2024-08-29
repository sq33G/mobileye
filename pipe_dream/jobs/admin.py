from django.contrib import admin
from .models import Job, RepoCredentials, Repo, DeployDestination, Run, Scheduling

admin.site.register((Job, RepoCredentials, Repo, DeployDestination, Run, Scheduling))