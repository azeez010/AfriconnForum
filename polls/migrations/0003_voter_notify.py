# Generated by Django 3.0.6 on 2020-08-16 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20200805_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='voter',
            name='notify',
            field=models.BooleanField(default=False),
        ),
    ]
