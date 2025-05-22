from rest_framework import serializers
from .models import Task, TaskChangeLog
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
class TaskChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChangeLog
        fields = '__all__'