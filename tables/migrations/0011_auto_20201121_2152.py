# Generated by Django 3.1 on 2020-11-21 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0010_auto_20201121_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='stud_photo',
            field=models.ImageField(null=True, upload_to='photos/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_temp_photo',
            field=models.ImageField(null=True, upload_to='photos/'),
        ),
    ]