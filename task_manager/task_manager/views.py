from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

from taskapp.serializers import TaskSerializer, TaskChangeLogSerializer
from taskapp.models import Task, TaskChangeLog

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['id', 'name', 'status', 'assigned_user']
    search_fields = ['name', 'description']

    def perform_update(self, serializer):
        old_info = self.get_object()

        old_data = {
            "name": old_info.name,
            "description": old_info.description,
            "status": old_info.status,
            "assigned_user": old_info.assigned_user.id if old_info.assigned_user else None
        }

        new_info = serializer.save()

        new_data = {
            "name": new_info.name,
            "description": new_info.description,
            "status": new_info.status,
            "assigned_user": new_info.assigned_user.id if new_info.assigned_user else None
        }

        TaskChangeLog.objects.create(
            task=new_info,
            old_data=old_data,
            new_data=new_data,
            user=self.request.user if self.request.user.is_authenticated else None
        )

    @action(detail=True, methods=['get'], url_path='history')
    def history(self, request, pk=None):
        task = self.get_object()
        logs = task.change_logs.all().order_by('-change_date')
        serializer = TaskChangeLogSerializer(logs, many=True)
        return Response(serializer.data)
