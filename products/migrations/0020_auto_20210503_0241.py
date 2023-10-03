# Generated by Django 3.1.7 on 2021-05-02 21:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0019_auto_20210503_0234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_date',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery',
            field=models.DateField(default='2021-01-01', verbose_name='Delivery Date'),
        ),
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 3, 2, 41, 7, 488142)),
        ),
    ]