# Generated by Django 3.0.6 on 2020-08-03 03:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_remove_thread_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='thread',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]