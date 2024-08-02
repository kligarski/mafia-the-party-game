from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    visible_username = models.CharField(max_length=40)
    last_activity = models.DateTimeField(auto_now=True)