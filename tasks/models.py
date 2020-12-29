from django.db import models
from django.contrib.auth.models import User


class New_Task(models.Model):
    task = models.CharField(max_length=500)
    dead_line = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    days = models.CharField(max_length=100, default='Deadline reached')

    def __str__(self):
        return self.task

