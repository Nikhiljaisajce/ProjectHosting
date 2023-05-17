# Generated by Django 3.1 on 2020-11-16 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='user_type',
            field=models.IntegerField(choices=[(0, 'admin'), (1, 'staff'), (2, 'department'), (3, 'student'), (4, 'party')]),
        ),
    ]
