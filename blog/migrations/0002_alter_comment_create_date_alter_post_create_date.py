# Generated by Django 5.1.7 on 2025-03-28 11:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 28, 11, 55, 41, 222080, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 28, 11, 55, 41, 222080, tzinfo=datetime.timezone.utc)),
        ),
    ]
