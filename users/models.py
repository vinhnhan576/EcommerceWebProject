from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    address = models.CharField(max_length=1000, default="Hanoi")
    phone = models.CharField(max_length=1000, default="0123456789")
    # class Meta:
    #     db_table = 'auth_user'