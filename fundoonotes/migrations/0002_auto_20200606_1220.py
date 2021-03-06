# Generated by Django 2.2.10 on 2020-06-06 06:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fundoonotes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='collaborator',
            field=models.ManyToManyField(blank=True, related_name='collaborator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='note',
            name='label',
            field=models.ManyToManyField(blank=True, related_name='label', to='fundoonotes.Label'),
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='label',
            name='user',
            field=models.ForeignKey(default=100, on_delete=django.db.models.deletion.CASCADE, related_name='label_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
