from distutils.command.upload import upload
from django.db import models
# Create your models here.
pv = [
    (0, 'admin'),
    (1, 'staff'),
    (2, 'department'),
    (3, 'student'),
    (4,'party')
]


class login(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=100)
    user_type = models.IntegerField(choices=pv)
    user_id = models.IntegerField()


class staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_fname = models.CharField(max_length=100)
    staff_mname = models.CharField(max_length=100)
    staff_lname = models.CharField(max_length=100)
    staff_email = models.EmailField(max_length=70)
    staff_phone = models.CharField(max_length=10)
    staff_status = models.IntegerField(default=0, choices=[(0, 'inactive'), (1, 'active')])


class department(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=100)
    dept_email = models.EmailField(max_length=70)
    dept_phone = models.CharField(max_length=20)


class course(models.Model):
    course_id = models.AutoField(primary_key=True)
    dept_id = models.ForeignKey(department, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=100)
    course_type = models.CharField(max_length=100)
    duration = models.IntegerField()

    
class student(models.Model):
    stud_id = models.IntegerField(primary_key=True)
    stud_fname = models.CharField(max_length=100)
    stud_mname = models.CharField(null=True,max_length=100)
    stud_lname = models.CharField(max_length=100)
    stud_dob = models.DateField(null=True)
    stud_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    stud_email = models.EmailField(max_length=70)
    stud_mob = models.CharField(null=True,max_length=11)
    stud_course_id = models.ForeignKey(course, on_delete=models.CASCADE)
    stud_start_date = models.DateField()
    stud_end_date = models.DateField()
    voter_status = models.IntegerField(null=True, choices=[(0, 'inactive'), (1, 'active')])
    staff_id = models.ForeignKey(staff,null=True,on_delete=models.DO_NOTHING)
    stud_photo = models.ImageField(null=True,upload_to='photos/')
    stud_temp_photo = models.ImageField(null=True,upload_to='photos/')
    stud_temp_mob = models.CharField(max_length=11, null=True)

class party(models.Model):
    party_id=models.AutoField(primary_key=True)
    party_name=models.CharField(max_length=100)
    party_email = models.EmailField(max_length=70, null=True)
    support_id=models.ForeignKey(student,null=True,on_delete=models.DO_NOTHING)
    support_status=models.IntegerField(null=True,default=0)
    party_status=models.IntegerField(default=0, choices=[(0, 'inactive'), (1, 'active')])

class election(models.Model):
    elect_id=models.AutoField(primary_key=True)
    elect_date=models.DateField()
    elect_nomi_start_date=models.DateField()
    elect_nomi_end_date=models.DateField()
    elect_nomi_withdrawal_end_date=models.DateField()
    elect_status = models.IntegerField(default=0)

class panel(models.Model):
    panel_id=models.AutoField(primary_key=True)
    panel_post=models.CharField(max_length=100)
    panel_type=models.IntegerField(default=0, choices=[(0, 'General'), (1, 'female')])
    panel_status=models.IntegerField(default=1, choices=[(0, 'inactive'), (1, 'active')])
    panel_year=models.IntegerField(default=0, choices=[(0, 'all'), (1, '1st year'), (2, '2nd year'), (3, '3rd year'), (4, '4th year')])
    panel_votes = models.IntegerField(default=1)

class panel_specific(models.Model):
    specific_id=models.AutoField(primary_key=True)
    panel_id=models.ForeignKey(panel,on_delete=models.CASCADE)
    course_id = models.ForeignKey(course, on_delete=models.CASCADE)


class election_panel(models.Model):
    ep_id=models.AutoField(primary_key=True)
    elect_id=models.ForeignKey(election,on_delete=models.CASCADE)
    panel_id=models.ForeignKey(panel,on_delete=models.CASCADE)

class symbol(models.Model):
    symbol_id=models.AutoField(primary_key=True)
    symbol_loc=models.ImageField(upload_to='symbols/')

class candidate(models.Model):
    cand_id=models.AutoField(primary_key=True)
    stud_id=models.ForeignKey(student,on_delete=models.CASCADE)
    party_id=models.ForeignKey(party,null=True,on_delete=models.CASCADE)
    ep_id=models.ForeignKey(election_panel,on_delete=models.CASCADE)
    symbol_id=models.ForeignKey(symbol,null=True,on_delete=models.CASCADE)
    cand_support_id1 = models.ForeignKey(student,null=True,related_name='support1',on_delete=models.DO_NOTHING)
    cand_support_id2 = models.ForeignKey(student,null=True, related_name='support2',on_delete=models.DO_NOTHING)
    cand_status=models.IntegerField(default=0, choices=[(0, 'inactive'), (1, 'active')])
    support_id1_status=models.IntegerField(default=0, choices=[(0, 'not approved'), (1, 'approved')])
    support_id2_status=models.IntegerField(default=0, choices=[(0, 'not approved'), (1, 'approved')])
    accept_sts=models.IntegerField(default=0,null=True)
    withdraw_status=models.IntegerField(default=0)


class vote(models.Model):
    vote_id=models.AutoField(primary_key=True)
    ep_id = models.ForeignKey(election_panel, on_delete=models.CASCADE)
    stud_id=models.ForeignKey(student,on_delete=models.DO_NOTHING)

class result(models.Model):
    res_id=models.AutoField(primary_key=True)
    ep_id=models.ForeignKey(election_panel,on_delete=models.CASCADE)
    cand_id=models.ForeignKey(candidate,on_delete=models.CASCADE)

class securevote(models.Model):
    stud_id = models.ForeignKey(student, on_delete=models.CASCADE)
    initState = models.IntegerField(default=0,null=True)
    remainingOtp = models.IntegerField(default=3)
    otp = models.CharField(max_length=6,default=None,null=True)
    completed = models.IntegerField(default=0,null=True)

class FeatureVector(models.Model):
    stud_id = models.ForeignKey(student, on_delete=models.CASCADE)
    fv_set = models.CharField(max_length=1400)
    