from .models import *
from .serializers import *
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters import DjangoFilterBackend, OrderingFilter

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