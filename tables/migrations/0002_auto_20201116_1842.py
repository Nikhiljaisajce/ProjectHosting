# Generated by Django 3.1 on 2020-11-16 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_phone',
            field=models.CharField(max_length=10),
        ),
    ]
