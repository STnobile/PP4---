# Generated by Django 3.2.19 on 2023-10-04 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_doc', '0009_auto_20231002_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='email',
            field=models.EmailField(max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='reschedule_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
