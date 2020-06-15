from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Fundoo(AbstractUser):
    upload = models.ImageField(null=True)


class SendMessage(models.Model):
    phone = models.CharField(max_length=15, blank=True)
