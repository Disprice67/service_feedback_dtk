# Generated by Django 4.2.16 on 2024-10-17 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_cases_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cases',
            name='activity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='api.actives_and_project'),
        ),
    ]
