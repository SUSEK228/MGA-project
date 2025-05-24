from rest_framework import serializers
from .models import Task, TaskChangeLog
from django.contrib.auth.models import User
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
    
        
class TaskChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskChangeLog
        fields = '__all__'
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
