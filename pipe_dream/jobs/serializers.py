from rest_framework import serializers
from .models import *

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'name', 'repo', 'schedule']

class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ['id', 'buildStatus', 'job', 'number']

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