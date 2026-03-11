from django.db import models
from datetime import datetime


class User(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return f"user id:{self.pk}"
