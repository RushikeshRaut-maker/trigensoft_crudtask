# Generated by Django 3.1.1 on 2021-10-19 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0002_auto_20211019_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='first_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='users',
            name='last_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='last name'),
        ),
    ]
