from rest_framework import serializers
from .models import *
from django.utils import timezone

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'repo', 'schedule', 'deployTo']

class RunSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['started'] = timezone.now()
        return super().create(validated_data)

    class Meta:
        model = Run
        fields = ['id', 'buildStatus', 'job', 'number', 'started', 'completed']

class RepoCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepoCredentials
        fields = ['id','name']

class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ['id','name','url','credentials']

class DeployDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeployDestination
        fields = ['id', 'name']