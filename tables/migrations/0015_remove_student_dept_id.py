# Generated by Django 3.1 on 2020-11-29 07:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0014_merge_20201129_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='dept_id',
        ),
    ]
