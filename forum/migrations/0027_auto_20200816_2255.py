# Generated by Django 3.0.6 on 2020-08-16 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0026_auto_20200816_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='sharer_id',
            new_name='sharer',
        ),
    ]