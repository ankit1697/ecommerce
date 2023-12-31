# Generated by Django 3.1.7 on 2021-05-10 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0044_auto_20210510_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 11, 0, 59, 46, 858361)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.DateField(default=datetime.date(2021, 5, 12), verbose_name='Delivery Date'),
        ),
    ]
