# Generated by Django 3.1.7 on 2021-05-02 21:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_auto_20210503_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 3, 2, 33, 15, 159712)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateField(default='01/01/2021'),
        ),
    ]
