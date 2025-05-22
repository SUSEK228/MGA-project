from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name=models.CharField(max_length=30)
    description = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('new', 'Nowy'),
        ('in_progress', 'W toku'),
        ('done', 'Rozwiązany'),
    ]
    status=models.CharField(max_length=50,choices=STATUS_CHOICES,default='new')
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class TaskChangeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='change_logs')
    change_date=models.DateTimeField(auto_now_add=True)
    old_data=models.JSONField()
    new_data=models.JSONField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Task {self.task.id} changed at {self.change_date}"

