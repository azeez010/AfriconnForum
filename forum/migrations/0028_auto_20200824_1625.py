# Generated by Django 3.0.6 on 2020-08-24 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0027_auto_20200816_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_url',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
