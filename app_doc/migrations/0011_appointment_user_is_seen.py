# Generated by Django 3.2.19 on 2023-10-04 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_doc', '0010_auto_20231004_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='user_is_seen',
            field=models.BooleanField(default=False),
        ),
    ]
