# Generated by Django 3.0.6 on 2020-08-14 19:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0022_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='datetime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
