# Generated by Django 4.2.5 on 2023-09-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api_app", "0002_vehicletimestamp"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicletimestamp",
            name="direction",
            field=models.CharField(
                choices=[("in", "In"), ("out", "Out")], max_length=5
            ),
        ),
    ]
