# Generated by Django 3.2.19 on 2023-06-21 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_doc', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='rescheduled',
            field=models.BooleanField(default=False),
        ),
    ]