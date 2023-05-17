# Generated by Django 3.1 on 2020-11-18 13:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0004_merge_20201117_1806'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='staff',
            name='staff_phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='student',
            name='staff_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tables.staff'),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_dob',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_mob',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_temp_mob',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='stud_temp_photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
