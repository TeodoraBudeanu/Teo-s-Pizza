# Generated by Django 2.2.4 on 2019-09-04 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
    ]