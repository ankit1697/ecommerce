# Generated by Django 3.1.7 on 2021-05-09 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_customeraddress_category_string'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=12, unique=True, verbose_name='Phone Number'),
        ),
    ]
