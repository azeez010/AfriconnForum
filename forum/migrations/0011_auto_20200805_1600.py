# Generated by Django 3.0.6 on 2020-08-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0010_auto_20200805_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='no_of_member',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='no_of_thread',
            field=models.IntegerField(default=0),
        ),
    ]
