# Generated by Django 2.2.4 on 2019-09-22 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expence_tracker', '0003_history_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='uid',
            field=models.CharField(max_length=150),
        ),
    ]
