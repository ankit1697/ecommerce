# Generated by Django 3.1.7 on 2021-05-02 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210502_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='customeraddress',
            name='selected',
            field=models.BooleanField(default=False),
        ),
    ]
