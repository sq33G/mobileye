"""
URL configuration for pipe_dream project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from jobs import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'runs', views.RunViewSet, basename='run')
router.register(r'deploy-destinations', views.DeployDestinationViewSet, basename='deploy-destination')
router.register(r'repos', views.RepoViewSet, basename='repo')
router.register(r'repo-credentials', views.RepoCredentialsViewSet, basename='repo-credentials')

urlpatterns = [
    path("admin/", admin.site.urls), 
    path("", include(router.urls))
    # path("api/auth", include("rest_framework.urls")) # for api auth
]

# not ideal to do this in such a random location, could do an endpoint instead?
from jobs.runner import Scheduler
alreadyScheduled = Scheduler.checkAlreadyRunning("jobs.tasks.check_schedule")
if alreadyScheduled:
    print('scheduler already set to run, cancel')
else:
    from jobs.tasks import check_schedule
    check_schedule(repeat=60)
