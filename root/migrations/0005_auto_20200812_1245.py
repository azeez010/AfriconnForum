# Generated by Django 3.0.6 on 2020-08-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('root', '0004_auto_20200812_1153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advert',
            name='ad_country',
            field=models.CharField(max_length=5),
        ),
    ]
