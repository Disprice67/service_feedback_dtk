# Generated by Django 2.2.19 on 2024-03-17 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0004_auto_20240317_2323'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='active_value',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='manager',
            name='manager_name',
            field=models.TextField(),
        ),
    ]
