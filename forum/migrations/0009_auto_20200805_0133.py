# Generated by Django 3.0.6 on 2020-08-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_onlineuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onlineuser',
            name='datetime',
        ),
        migrations.AddField(
            model_name='onlineuser',
            name='last_seen',
            field=models.IntegerField(default=0),
        ),
    ]