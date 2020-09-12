from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Report(models.Model):
    """A Class representing Report Model

    Args: models: A Class Model of Django """
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude  = models.FloatField()
    accuracy = models.FloatField(blank=True, null=True)
    creation_time = models.DateTimeField(default=datetime.now, blank=True)
    update_time = models.DateTimeField(default=datetime.now, blank=True)

    def save(self, *args, **kwargs):
        """Modify save method"""
        # Set always update update_time
        self.update_time = datetime.now()
        super().save(*args, **kwargs)
