# Generated by Django 2.2.3 on 2019-07-25 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0018_auto_20190725_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='confirmed',
            field=models.BooleanField(default=False),
        ),
    ]