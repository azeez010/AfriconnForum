# Generated by Django 3.0.6 on 2020-08-03 03:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='category',
        ),
    ]
