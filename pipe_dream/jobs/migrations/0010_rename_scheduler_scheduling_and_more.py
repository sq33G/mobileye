# Generated by Django 5.1 on 2024-08-28 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_scheduler'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Scheduler',
            new_name='Scheduling',
        ),
        migrations.RenameField(
            model_name='scheduling',
            old_name='lastSuccessfulScheduling',
            new_name='lastSuccessful',
        ),
    ]
