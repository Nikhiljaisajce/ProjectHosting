# Generated by Django 3.1 on 2020-11-18 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0005_auto_20201118_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_phone',
            field=models.CharField(max_length=20),
        ),
    ]
