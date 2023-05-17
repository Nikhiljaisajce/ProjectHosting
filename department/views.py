from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
# Create your views here.
from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.http import JsonResponse
from tables.models import *
from django.db.models import Q
# for otp
import math, random

def getName(request):
    t_did = request.session['id']
    t_d = department.objects.get(dept_id=t_did)
    t_name = t_d.dept_name
    return  t_name

def home(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    t_name = getName(request)
    return render(request, 'department/master.html',{'name':t_name})


def addstud(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = election.objects.filter(elect_status=0)
    if obj.count() >0:
        messages.success(request, "Access denied due to Election!")
        return redirect('http://127.0.0.1:8000/home/department/')

    did = request.session['id']
    c = course.objects.filter(dept_id_id=did)
    if request.method == 'POST':
        id = request.POST.get('id')
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        gen = request.POST.get('gen')
        co = request.POST.get('cr')
        sdate = request.POST.get('startdate')
        edate = request.POST.get('enddate')
        email = request.POST.get('email')
        s = student.objects.filter(stud_email=email)
        if s.count() == 0:
            s = student(stud_id=id,stud_fname=fname, stud_mname=mname, stud_lname=lname, stud_gender=gen, stud_email=email,
                        stud_start_date=sdate, stud_end_date=edate, stud_course_id_id=co, voter_status="1")
            s.save()
            user = "stud" + str(s.stud_id)
            pwd = "stud" + str(s.stud_id)
            print(s.stud_id)
            l = login(username=user, password=pwd, user_type=3, user_id=s.stud_id)
            l.save()
            subject = 'College_Election - Student Login Details'
            if mname == '':
                message = 'Dear ' + fname + ' ' + lname + '\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd
            else:
                message = 'Dear ' + fname + ' ' + mname + ' ' + lname + '\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd

            message += '\nNote: Please use forgot password option to change your password!'
            recepient = str(email)
            print(message)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            messages.success(request, "Student Details Saved")
    t_name = getName(request)
    return render(request, 'department/StudAdd.html', {'courses': c, 'name':t_name})


def addcourse(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = election.objects.filter(elect_status=0)
    if obj.count() > 0:
        messages.success(request, "Access denied due to Election!")
        return redirect('http://127.0.0.1:8000/home/department/')

    did = request.session['id']
    if request.method == 'POST':
        cname = request.POST.get('cname')
        ctype = request.POST.get('ctype')
        dur = int(request.POST.get('dur'))

        # d=department.objects.filter(dept_id=did)
        # for q in d:
        c = course(course_name=cname, course_type=ctype, duration=dur, dept_id_id=did)
        c.save()
        messages.success(request, "Course Saved")
    t_name = getName(request)
    cobj = course.objects.filter(dept_id_id=request.session['id'])

    return render(request, 'department/CourseAdd.html', {'name':t_name,'c':cobj})


def courseedit(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = election.objects.filter(elect_status=0)
    if obj.count() > 0:
        messages.success(request, "Access denied due to Election!")
        return redirect('http://127.0.0.1:8000/home/department/')

    did = request.session['id']
    d = department.objects.filter(dept_id=did)
    c = course.objects.filter(dept_id=did)

    if request.method == "POST":
        dur = request.POST['course_dur']
        cid = request.POST['course']
        course.objects.filter(course_id=cid).update(duration=dur)
        messages.success(request, "Course Deatils Updated")

    t_name = getName(request)
    return render(request, 'department/CourseEdit.html', {'dept': d, 'course': c,'name':t_name})


def deptedit(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    did = request.session['id']
    d = department.objects.filter(dept_id=did)
    t_name = getName(request)
    if request.method == 'POST':
        keys = request.session.keys()
        postKeys = request.POST.keys()
        if 'oldOtp' in postKeys:
            if 'mobOtp' in keys:
                if request.session['mobOtp'] != request.POST['oldOtp']:
                    messages.success(request, "OTP Verification Failed!")
                    return render(request, 'department/DeptEdit.html', {'dept': d, 'name':t_name})

        if 'oldOtp' in postKeys:
            if 'oldMailOtp' in keys:
                if request.session['oldMailOtp'] != request.POST['oldOtp']:
                    messages.success(request, "OTP Verification Failed!")
                    return render(request, 'department/DeptEdit.html', {'dept': d,'name':t_name})
        if 'newOtp' in postKeys:
            if 'newMailOtp' in keys:
                if request.session['newMailOtp'] != request.POST['newOtp']:
                    messages.success(request, "OTP Verification Failed!")
                    return render(request, 'department/DeptEdit.html', {'dept': d, 'name':t_name})
        dmail = request.POST['dmail']
        dmob = request.POST['txtPhone']
        department.objects.filter(dept_id=did).update(dept_email=dmail, dept_phone=dmob)
        messages.success(request, "Modifications Saved")

    return render(request, 'department/DeptEdit.html', {'dept': d,'name':t_name})


def validate_addstud(request):
    email = request.GET.get('email')
    s = student.objects.filter(stud_email=email)
    dmail_status = False
    if s.count() > 0:
        dmail_status = True
    data = {
        'dmail_status': dmail_status
    }
    return JsonResponse(data)


def validate_addcourse(request):
    cname = request.GET.get('email')
    s = course.objects.filter(course_name=cname,dept_id=request.session['id'])
    dmail_status = False
    if s.count() > 0:
        dmail_status = True
    data = {
        'dmail_status': dmail_status
    }
    return JsonResponse(data)


def validate_dept_edit(request):
    dmail = request.GET.get('dmail')
    dmob = request.GET.get('dmob')
    did = request.session['id']
    for key in list(request.session.keys()):
        if  key.startswith("oldMailOtp"):  # skip keys set by the django system
            del request.session[key]
        if  key.startswith("newMailOtp"):  # skip keys set by the django system
            del request.session[key]
        if  key.startswith("mobOtp"):  # skip keys set by the django system
            del request.session[key]
    d = department.objects.filter(dept_id=did)

    dmobStatus = False
    dmailStatus = False
    dexist = False

    d1 = department.objects.filter(~Q(dept_id=did))
    for j in d1:
            if j.dept_email == dmail:
                dexist = True
                data = {
                    'dmail_status': dmailStatus,
                    'dmob_status': dmobStatus,
                    'dexist': dexist
                }
                return JsonResponse(data)

    if d.count() > 0:
        for obj in d:
            if (dmail == obj.dept_email) and (dmob == obj.dept_phone):
                dexist = True
                data = {
                    'dmail_status': dmailStatus,
                    'dmob_status': dmobStatus,
                    'dexist' : dexist
                }
                return JsonResponse(data)

            if (dmail != obj.dept_email) and (dmob != obj.dept_phone):
                oldMailOtp = OTPgenerator()
                newMailOtp = OTPgenerator()
                sendOtpToMAil(obj.dept_email, oldMailOtp, 'old')
                sendOtpToMAil(dmail, newMailOtp, 'new')
                request.session['newMailOtp'] = newMailOtp
                request.session['oldMailOtp'] = oldMailOtp
                dmailStatus = True
                dmobStatus = True
            elif dmail != obj.dept_email:  # new mail so otp need to old and new mail
                oldMailOtp = OTPgenerator()
                newMailOtp = OTPgenerator()
                sendOtpToMAil(obj.dept_email,oldMailOtp,'old')
                sendOtpToMAil(dmail, newMailOtp,'new')
                request.session['newMailOtp'] = newMailOtp
                request.session['oldMailOtp'] = oldMailOtp
                dmailStatus = True


            elif dmob != obj.dept_phone:  # new mobile so otp to old mail
                mobOtp = OTPgenerator()
                sendOtpToMAil(obj.dept_email, mobOtp, 'mob')
                request.session['mobOtp'] = mobOtp
                dmobStatus = True

            data = {
                'dmail_status' : dmailStatus,
                'dmob_status'  : dmobStatus
            }
            break
        return  JsonResponse(data)

def OTPgenerator():
    digits_in_otp = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(digits_in_otp)
    for i in range(6):
        OTP += digits_in_otp[math.floor(random.random() * length)]

    print("otp is : ", OTP)

    return OTP

def sendOtpToMAil(mailAddr, otp,msg):
    subject = 'College_Election - OTP for Department Edit Verification'
    if msg=='old':
        message = 'Hello,\nYour One Time Password for changing '+str(mailAddr)+' to new Mail id is\n'+ str(otp)
    if msg=='new':
        message = 'Hello,\nYour One Time Password for activating ' + str(mailAddr) + ' is\n' + str(otp)
    if msg=='mob':
        message = 'Hello,\nYour One Time Password for changing mobile number is \n'+ str(otp)
    mailAddr = str(mailAddr)
    recepient = str(mailAddr)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)


def upload(request):
    if "GET" == request.method:
        return render(request, 'department/upload.html', {})
    if request.method == "POST":
        csv_file = request.FILES["csv_upload"]
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, 'the wrong file is uploaded')
            #return redirect('/admin/')

        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")
        status = "false"
        for x in csv_data:
            fields = x.split(",")
            #print(fields)
            csv_data_dict=dict(enumerate(fields))
            print("Debug 1 : "+csv_data_dict.get(0))

            #a = stud(stud_id=csv_data_dict.get(0),stud_fname=csv_data_dict.get(1),stud_lname=csv_data_dict.get(2),stud_dob=csv_data_dict.get(3),stud_gender=csv_data_dict.get(4),stud_email=csv_data_dict.get(5),stud_mob=csv_data_dict.get(6),stud_start_date=csv_data_dict.get(7),stud_end_date=csv_data_dict.get(8),stud_course_id_id=csv_data_dict.get(9))
            #a.save()
          
            #if tbl_login.objects.filter(email=fields[5], uid=fields[0]).exists():
                #messages.warning(request, "---unsuccessfull,person already exists---")
            #else:
                #a = tbl_login(uid=fields[0], email=fields[5], password=fields[6], type="student")
                #a.save()
                #user = tbl_login.objects.get(email=fields[5])
                #b = tbl_reg(person=user, first_name=fields[1], last_name=fields[2], mobile=fields[3], depart=fields[4])
                #b.save()
            id=csv_data_dict.get(0)
            fname = csv_data_dict.get(1)
            mname = csv_data_dict.get(2)
            lname = csv_data_dict.get(3)
            gen = csv_data_dict.get(4)
            co = csv_data_dict.get(8)
            sdate = csv_data_dict.get(6)
            edate = csv_data_dict.get(7)
            email = csv_data_dict.get(5)
            s = student.objects.filter(stud_email=email)
            if id =='':
                continue
            if s.count() ==0:
                s = student(stud_id=id,stud_fname=fname, stud_mname=mname, stud_lname=lname, stud_gender=gen, stud_email=email, stud_start_date=sdate, stud_end_date=edate, stud_course_id_id=co, voter_status="1")
                print(id+" id")
                s.save()
                user = "stud" + str(s.stud_id)
                pwd = "stud" + str(s.stud_id)
                l = login(username=user, password=pwd, user_type=3, user_id=s.stud_id)
                l.save()
                subject = 'College_Election - Student Login Details'
                if mname == '':
                    message = 'Dear ' + fname + ' ' + lname + '\nYour login credentials for http://127.0.0.1:8000/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd
                else:
                    message = 'Dear ' + fname + ' ' + mname + ' ' + lname + '\nYour login credentials for http://127.0.0.1:8000/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd

                message += '\nNote: Please use forgot password option to change your password!'
                recepient = str(email)
                print(message)
                print("R1 " + recepient +  "recepients")
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
                # messages.success(request, "Student Details Saved")
                if status !="true":
                    status ="true"
        if status =='true':
            messages.success(request,'Upload Successfully')
    return render(request, 'department/upload.html', {})

def studReport(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    id=request.session['id']
    obj = student.objects.filter(stud_course_id__dept_id=id)
    if obj.count()==0:
        messages.success(request, "Student list is empty!")
        return redirect('http://127.0.0.1:8000/home/department')

    return render(request, 'department/Studrpt.html',{'dept': obj, })

def studReport(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    id=request.session['id']
    obj = student.objects.filter(stud_course_id__dept_id=id)
    if obj.count()==0:
        messages.success(request, "Student list is empty!")
        return redirect('http://127.0.0.1:8000/home/department')

    return render(request, 'department/Studrpt.html',{'dept': obj, })