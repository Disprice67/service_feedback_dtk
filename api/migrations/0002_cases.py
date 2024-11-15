# Generated by Django 4.2.16 on 2024-10-17 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField()),
                ('priority', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('theme', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('executor', models.CharField(max_length=100)),
                ('activity_code', models.CharField(max_length=20)),
                ('activity_name', models.CharField(max_length=255)),
                ('resolution_description', models.TextField()),
            ],
        ),
    ]
