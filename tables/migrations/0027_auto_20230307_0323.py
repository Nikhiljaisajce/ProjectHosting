# Generated by Django 3.1.7 on 2023-03-06 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0026_auto_20230303_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stud',
            old_name='admno',
            new_name='stud_course_id_id',
        ),
        migrations.RenameField(
            model_name='stud',
            old_name='batch',
            new_name='stud_dob',
        ),
        migrations.RenameField(
            model_name='stud',
            old_name='email',
            new_name='stud_email',
        ),
        migrations.RenameField(
            model_name='stud',
            old_name='fname',
            new_name='stud_end_date',
        ),
        migrations.RenameField(
            model_name='stud',
            old_name='gender',
            new_name='stud_fname',
        ),
        migrations.RenameField(
            model_name='stud',
            old_name='lname',
            new_name='stud_gender',
        ),
        migrations.RenameField(
            model_name='stud',
            old_name='sem',
            new_name='stud_id',
        ),
        migrations.AddField(
            model_name='stud',
            name='stud_lname',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='stud',
            name='stud_mname',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='stud',
            name='stud_mob',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='stud',
            name='stud_start_date',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
