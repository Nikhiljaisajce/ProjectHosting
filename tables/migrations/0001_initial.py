# Generated by Django 3.1 on 2020-11-14 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='candidate',
            fields=[
                ('cand_id', models.AutoField(primary_key=True, serialize=False)),
                ('cand_status', models.IntegerField(choices=[(0, 'inactive'), (1, 'active')], default=0)),
                ('support_id1_status', models.IntegerField(choices=[(0, 'not approved'), (1, 'approved')], default=0)),
                ('support_id2_status', models.IntegerField(choices=[(0, 'not approved'), (1, 'approved')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_name', models.CharField(max_length=100)),
                ('course_type', models.CharField(max_length=100)),
                ('duration', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('dept_id', models.AutoField(primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=100)),
                ('dept_email', models.EmailField(max_length=70)),
                ('dept_phone', models.IntegerField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='election',
            fields=[
                ('elect_id', models.AutoField(primary_key=True, serialize=False)),
                ('elect_date', models.DateField()),
                ('elect_nomi_start_date', models.DateField()),
                ('elect_nomi_end_date', models.DateField()),
                ('elect_nomi_withdrawal_end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='election_panel',
            fields=[
                ('ep_id', models.AutoField(primary_key=True, serialize=False)),
                ('elect_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.election')),
            ],
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=100)),
                ('user_type', models.IntegerField(choices=[(0, 'admin'), (1, 'staff'), (2, 'department'), (3, 'student')])),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='panel',
            fields=[
                ('panel_id', models.AutoField(primary_key=True, serialize=False)),
                ('panel_post', models.CharField(max_length=100)),
                ('panel_type', models.IntegerField(choices=[(0, 'General'), (1, 'female')], default=0)),
                ('panel_status', models.IntegerField(choices=[(0, 'inactive'), (1, 'active')], default=0)),
                ('panel_year', models.IntegerField(choices=[(0, 'all'), (1, '1st year'), (2, '2nd year'), (3, '3rd year'), (4, '4th year')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='staff',
            fields=[
                ('staff_id', models.AutoField(primary_key=True, serialize=False)),
                ('staff_fname', models.CharField(max_length=100)),
                ('staff_mname', models.CharField(max_length=100)),
                ('staff_lname', models.CharField(max_length=100)),
                ('staff_email', models.EmailField(max_length=70)),
                ('staff_phone', models.IntegerField(max_length=10)),
                ('staff_status', models.IntegerField(choices=[(0, 'inactive'), (1, 'active')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('stud_id', models.AutoField(primary_key=True, serialize=False)),
                ('stud_fname', models.CharField(max_length=100)),
                ('stud_mname', models.CharField(max_length=100)),
                ('stud_lname', models.CharField(max_length=100)),
                ('stud_dob', models.DateField()),
                ('stud_gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('stud_email', models.EmailField(max_length=70)),
                ('stud_mob', models.IntegerField(max_length=10)),
                ('stud_start_date', models.DateField()),
                ('stud_end_date', models.DateField()),
                ('voter_status', models.IntegerField(choices=[(0, 'inactive'), (1, 'active')], default=0)),
                ('stud_photo', models.ImageField(upload_to='')),
                ('stud_temp_photo', models.ImageField(upload_to='')),
                ('stud_temp_mob', models.IntegerField(max_length=10)),
                ('dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.department')),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tables.staff')),
                ('stud_course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.course')),
            ],
        ),
        migrations.CreateModel(
            name='symbol',
            fields=[
                ('symbol_id', models.AutoField(primary_key=True, serialize=False)),
                ('symbol_loc', models.ImageField(upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='vote',
            fields=[
                ('vote_id', models.AutoField(primary_key=True, serialize=False)),
                ('ep_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.election_panel')),
                ('stud_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tables.student')),
            ],
        ),
        migrations.CreateModel(
            name='result',
            fields=[
                ('res_id', models.AutoField(primary_key=True, serialize=False)),
                ('cand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.candidate')),
                ('ep_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.election_panel')),
            ],
        ),
        migrations.CreateModel(
            name='party',
            fields=[
                ('party_id', models.AutoField(primary_key=True, serialize=False)),
                ('party_name', models.CharField(max_length=100)),
                ('party_status', models.IntegerField(choices=[(0, 'inactive'), (1, 'active')], default=0)),
                ('support_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tables.student')),
            ],
        ),
        migrations.CreateModel(
            name='panel_specific',
            fields=[
                ('specific_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.course')),
                ('panel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.panel')),
            ],
        ),
        migrations.AddField(
            model_name='election_panel',
            name='panel_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.panel'),
        ),
        migrations.AddField(
            model_name='course',
            name='dept_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.department'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='cand_support_id1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='support1', to='tables.student'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='cand_support_id2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='support2', to='tables.student'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='ep_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.election_panel'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='party_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.party'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='stud_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.student'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='symbol_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.symbol'),
        ),
    ]