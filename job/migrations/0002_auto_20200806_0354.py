# Generated by Django 3.0.6 on 2020-08-06 02:54

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='details',
            field=tinymce.models.HTMLField(),
        ),
    ]
