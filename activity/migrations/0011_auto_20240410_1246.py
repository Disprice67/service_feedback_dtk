# Generated by Django 2.2.19 on 2024-04-10 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_auto_20240328_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='fourth_question',
            field=models.CharField(choices=[('1', 'Да'), ('0', 'Нет')], default='0', max_length=1),
        ),
        migrations.AlterField(
            model_name='manager',
            name='third_question',
            field=models.CharField(choices=[('1', 'Да'), ('0', 'Нет')], default='0', max_length=1),
        ),
    ]
