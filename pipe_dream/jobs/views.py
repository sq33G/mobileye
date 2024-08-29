from .models import *
from .serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = JobSerializer
    filterset_fields = ['name', 'repo']
    ordering_fields = ['name', 'repo', 'schedule']
    ordering = ['schedule', 'name']

class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = RunSerializer
    filterset_fields = ['buildStatus', 'job']
    ordering_fields = ['buildStatus', 'job', 'number', 'started', 'completed']
    ordering = ['-started']

class DeployDestinationViewSet(viewsets.ModelViewSet):
    queryset = DeployDestination.objects.all()
    serializer_class = DeployDestinationSerializer

class RepoViewSet(viewsets.ModelViewSet):
    queryset = Repo.objects.all()
    serializer_class = RepoSerializer

class RepoCredentialsViewSet(viewsets.ModelViewSet):
    queryset = RepoCredentials.objects.all() #ideally, do a more limited view here 
    serializer_class = RepoCredentialsSerializer

class NotificationDestinationViewSet(viewsets.ModelViewSet):
    queryset = NotifyDestination.objects.all()
    serializer_class = NotifyDestinationSerializer