# Generated by Django 3.0.6 on 2020-08-04 23:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ip', models.CharField(max_length=2000)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
        ),
    ]
