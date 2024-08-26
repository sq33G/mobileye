from django.contrib import admin
from .models import Job, RepoCredentials, Repo

admin.site.register(Job)
admin.site.register(RepoCredentials)
admin.site.register(Repo)