# Generated by Django 2.2.4 on 2019-08-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20190827_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('O', 'Open'), ('C', 'Confirmed'), ('P', 'Paid'), ('D', 'Delivered')], default='O', max_length=1),
        ),
    ]
