# Generated by Django 4.2.6 on 2023-10-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("uavs", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="uav",
            name="hourly_rate",
            field=models.FloatField(default=0.0, help_text="USD"),
        ),
    ]
