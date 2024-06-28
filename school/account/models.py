from typing import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    birthdate = models.DateField()
    role = models.CharField(max_length=100,choices=(('teacher','teacher'),('admin','admin'),('student','student')))
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)
        
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)