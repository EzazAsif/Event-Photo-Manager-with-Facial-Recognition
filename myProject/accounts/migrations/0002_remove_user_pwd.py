# Generated by Django 5.0.4 on 2024-11-03 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='pwd',
        ),
    ]