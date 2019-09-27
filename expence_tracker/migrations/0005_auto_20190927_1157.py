# Generated by Django 2.2.4 on 2019-09-27 06:27

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('expence_tracker', '0004_auto_20190922_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='history',
            name='p_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='history',
            name='p_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
