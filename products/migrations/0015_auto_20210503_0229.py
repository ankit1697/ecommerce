# Generated by Django 3.1.7 on 2021-05-02 20:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20210502_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 3, 2, 29, 33, 688328)),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.TimeField(),
        ),
    ]
