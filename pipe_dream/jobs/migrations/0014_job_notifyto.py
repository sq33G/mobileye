# Generated by Django 5.1 on 2024-08-29 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_notifydestination'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='notifyTo',
            field=models.ManyToManyField(blank=True, to='jobs.notifydestination'),
        ),
    ]
