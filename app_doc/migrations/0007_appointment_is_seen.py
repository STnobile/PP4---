# Generated by Django 3.2.19 on 2023-10-01 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_doc', '0006_alter_appointment_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
