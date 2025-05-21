from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from taskapp.serializers import TaskSerializer
from taskapp.models import Task

class TaskViewSet(viewsets.ModelViewSet):
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'name', 'status', 'assigned_user']
    search_fields = ['name', 'description']
