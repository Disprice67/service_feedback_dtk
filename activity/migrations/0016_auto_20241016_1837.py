# Generated by Django 2.2.19 on 2024-10-16 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0015_auto_20241016_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(default=None),
        ),
    ]
