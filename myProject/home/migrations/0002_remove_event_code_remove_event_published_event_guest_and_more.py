# Generated by Django 5.0.4 on 2024-11-03 07:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='code',
        ),
        migrations.RemoveField(
            model_name='event',
            name='published',
        ),
        migrations.AddField(
            model_name='event',
            name='guest',
            field=models.ManyToManyField(related_name='guest_events', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='userPicsRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.picsrelation')),
                ('user', models.ManyToManyField(related_name='guest_pics', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]