# Generated by Django 3.1.7 on 2021-05-09 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20210509_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=12, verbose_name='Phone Number'),
        ),
    ]