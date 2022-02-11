from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid
from datetime import datetime, timedelta

class User(AbstractUser):

    @property
    def is_online(self):
        return self.online.last_activity > datetime.now() - timedelta(minutes=5)


class UserRegistration(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4())
    approve = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)


class UserOnline(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='online')
    last_activity = models.DateTimeField(auto_now=True)