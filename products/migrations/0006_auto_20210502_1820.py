# Generated by Django 3.1.7 on 2021-05-02 12:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210502_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 2, 18, 20, 5, 603166)),
        ),
    ]