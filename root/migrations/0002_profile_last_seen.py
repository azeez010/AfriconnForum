# Generated by Django 3.0.6 on 2020-08-07 14:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_seen',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]