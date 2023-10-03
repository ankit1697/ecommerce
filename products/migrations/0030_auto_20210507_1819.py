# Generated by Django 3.1.7 on 2021-05-07 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_auto_20210506_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 7, 18, 19, 36, 566246)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.DateField(default=datetime.date(2021, 5, 7), verbose_name='Delivery Date'),
        ),
    ]
