# Generated by Django 3.0.6 on 2020-08-06 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0012_auto_20200805_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='members',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('chat_receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_receiver', to=settings.AUTH_USER_MODEL)),
                ('chat_sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_sender', to=settings.AUTH_USER_MODEL)),
                ('who_send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_send', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
