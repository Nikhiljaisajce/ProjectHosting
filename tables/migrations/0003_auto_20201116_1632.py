# Generated by Django 3.1 on 2020-11-16 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0002_auto_20201116_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_phone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_phone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_mob',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_temp_mob',
            field=models.IntegerField(),
        ),
    ]