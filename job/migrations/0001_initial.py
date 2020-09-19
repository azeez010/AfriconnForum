# Generated by Django 3.0.6 on 2020-08-03 02:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=450)),
                ('details', models.TextField()),
                ('address', models.CharField(max_length=4000)),
                ('name_of_company', models.CharField(max_length=450)),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('slugTitle', models.CharField(max_length=450)),
                ('fulfilled', models.BooleanField(default=False)),
                ('pay', models.IntegerField(default=0)),
                ('position', models.CharField(max_length=450)),
                ('jobImage', models.ImageField(blank=True, default='./forum/static/portofolio.png', upload_to='job_images')),
                ('category', models.CharField(max_length=450)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applydate', models.DateTimeField()),
                ('doc', models.FileField(blank=True, upload_to='job_files')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AlreadyApplied',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]