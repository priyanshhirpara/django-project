from django.db import models
from account.models import CustomUser
from competition.models import CompetitionModels
from django.utils import timezone


# Create your models here.
class EntryModels(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    submission = models.DateField()
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    competition = models.ForeignKey(CompetitionModels,on_delete=models.CASCADE)
    created_by = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_by = models.CharField(max_length=255, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()

        return super().save(*args, **kwargs)