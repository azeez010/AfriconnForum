# Generated by Django 3.0.6 on 2020-08-24 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0005_auto_20200812_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='advert_image_url',
            field=models.CharField(default='', max_length=800),
        ),
    ]