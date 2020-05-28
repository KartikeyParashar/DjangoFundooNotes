from django.db import models

# Create your models here.
from django.db import models
from users.models import Fundoo


class Label(models.Model):
    user = models.ForeignKey(Fundoo, on_delete=
                             models.CASCADE, related_name='label_user', default=100)
    name = models.CharField("name_of_label", max_length=49)

    def __str__(self):
        return self.name


class Note(models.Model):
    user = models.ForeignKey(Fundoo, on_delete=models.CASCADE, related_name='user', null=True)
    title = models.CharField(max_length=999, blank=True)
    note = models.CharField(max_length=2999)
    label = models.ManyToManyField(Label, related_name='label', blank=True)
    collaborator = models.ManyToManyField(Fundoo, related_name='collaborator', blank=True)
    image = models.ImageField(blank=True, null=True, upload_to='media')
    reminder = models.DateTimeField(blank=True, null=True)
    color = models.CharField(blank=True, null=True, max_length=10)
    is_archive = models.BooleanField("is_archive", default=False)
    is_trashed = models.BooleanField("is_trashed", default=False)
    is_pin = models.BooleanField("is_pin", default=False)

    def __str__(self):
        return self.title

