# Generated by Django 3.2.19 on 2023-10-11 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_doc', '0014_auto_20231009_1301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='is_seen',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='user_is_seen',
        ),
    ]