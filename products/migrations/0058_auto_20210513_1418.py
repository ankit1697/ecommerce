# Generated by Django 3.1.7 on 2021-05-13 08:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0057_auto_20210513_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.AlterField(
            model_name='order',
            name='cancelled_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 13, 14, 18, 19, 946391)),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
