from django.shortcuts import render, redirect
from django.http import  HttpResponseRedirect
from tables.models import *
from django.db.models import Q, Count
from django.contrib import messages
import datetime, math, random
from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from matplotlib import pyplot as plt

from django.http import HttpResponse


# Create your views here.
def home(request):
    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]

    e = election.objects.filter(elect_status=0)
    menuHide = 0
    elect_status = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1
    if e.count() != 0:
        elect_status = 1
        return render(request, 'home/master.html/',{'menuHide':menuHide,'elect_status':elect_status,'ee':e[0]})
    return render(request, 'home/master.html/', {'menuHide': menuHide, 'elect_status': elect_status})


def Login(request):
    for key in list(request.session.keys()):
        if not key.startswith("_"):  # skip keys set by the django system
            del request.session[key]
    if request.method == 'POST':
        uname = request.POST['uname']
        pwd = request.POST['pass']
        u = login.objects.filter(Q(username=uname) & Q(password=pwd))
        if u:
            request.session['id'] = u[0].user_id
            if u[0].user_type == 0:
                return redirect('http://127.0.0.1:8000/home/admin/')
            elif u[0].user_type == 1:
                s = staff.objects.get(staff_id=request.session['id'])
                if s.staff_status==0:
                    messages.success(request, "Access Denied. Your account is deactivated.")
                    return redirect('http://127.0.0.1:8000/home/login/')
                else:
                    return redirect('http://127.0.0.1:8000/home/staff/')
            elif u[0].user_type == 2:
                return redirect('http://127.0.0.1:8000/home/department/')
            elif u[0].user_type == 3:
                s = student.objects.get(stud_id=request.session['id'])
                if s.stud_end_date < datetime.date.today():
                    messages.success(request, "Access Denied. You are not studying in collage currently")
                    return redirect('http://127.0.0.1:8000/home/login/')
                else:
                    return redirect('http://127.0.0.1:8000/home/student/')
            else:
                return redirect('http://127.0.0.1:8000/home/party/')

        else:
            messages.success(request, "Invalid Username or Password")

    e = election.objects.filter(elect_status=0)
    menuHide = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1
    return render(request, 'home/login.html/',{'menuHide':menuHide})


def party_reg(request):
    if request.method == 'POST':
        pname = request.POST.get('pname')
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        spid = request.POST.get('sprt')
        mail = request.POST.get('dmail')
        obj = login.objects.filter(username=uname)
        if obj.count() == 0:
            p1 = party.objects.filter(party_email=mail)
            if p1.count() > 0:
                messages.success(request, "Mail Address Already Exists!")
            else:
                p = party(party_name=pname, support_id_id=spid, party_email=mail)
                p.save()
                l = login(username=uname, password=pwd, user_type=4, user_id=p.party_id)
                l.save()

                subject = 'College_Election - Party Login Details'
                message = '\nYour party registration has been succeeded'
                message += '\nUser Name:' + uname + '\nPassword:' + pwd
                recepient = str(mail)
                send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
                messages.success(request, "Student Organization Registration Success")
                return redirect('http://127.0.0.1:8000/home/login/')
        else:
            messages.success(request, "Username Alreadyff Exists!")

    if party.objects.all().count() > 0:
        ps = party.objects.values('support_id_id')
        pss = party.objects.filter(support_status=None).values('support_id_id')
        s = student.objects.filter(Q(voter_status=1) & Q(~Q(stud_id__in=ps) | Q(stud_id__in=pss)))
    else:
        s = student.objects.filter(voter_status=1)

    s = s.filter(stud_end_date__gt=datetime.date.today())
    c = course.objects.all()

    e = election.objects.filter(elect_status=0)
    menuHide = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1

    return render(request, 'home/partyadd.html/', {'sid': s, 'course': c,'menuHide':menuHide})


def electResults(request):
    e = election.objects.all()
    if e.count() == 0:
        messages.success(request, "Elections Not Found")
        return redirect('http://127.0.0.1:8000/home/')
    e = election.objects.filter(elect_status=0)
    if e.count() == 0:
        pass
    else:
        td = datetime.date.today()
        if td < e[0].elect_date:
            messages.success(request, "Election date is " + str(e[0].elect_date))
            return redirect('http://127.0.0.1:8000/home/')
        t = datetime.datetime.now()
        if t.hour <= 8:
            messages.success(request, "Voting starts at 9am!")
            return redirect('http://127.0.0.1:8000/home/')
        if t.hour <= 12:
            messages.success(request, "Voting ends at 1pm!")
            return redirect('http://127.0.0.1:8000/home/')
        if e.count() > 0:
            messages.success(request, "Result Not Published Yet")
            return redirect('http://127.0.0.1:8000/home/')

    eobj = election.objects.all().last()
    ele_id = eobj.elect_id
    epanel_ids_for_elect = election_panel.objects.filter(elect_id=eobj.elect_id)
    epanel_ids = []

    for i in epanel_ids_for_elect:
        # """ election_panel ids for current election """
        epanel_ids.append(i.ep_id)

    epanel_ids1 = []  # ep_id with 1 or more candidates
    for i in epanel_ids:
        cand = candidate.objects.filter(ep_id_id=i, cand_status=1)
        if cand.count() > 0:
            epanel_ids1.append(i)

    candList = []  # candidates with no opponent objects
    candList1 = []  # candidates with opponent objects


    for i in epanel_ids1:
        cand1 = candidate.objects.filter(ep_id_id=i)
        if cand1.count() != 0:
            if cand1.count() <= election_panel.objects.get(ep_id=i).panel_id.panel_votes:
                for j in cand1:
                    candList.append(j)
            elif cand1.count() > election_panel.objects.get(ep_id=i).panel_id.panel_votes:
                for j in cand1:
                    candList1.append(j)


    resSet={}

    for i in candList1:             # votes counting
        res = result.objects.filter(cand_id=i)
        resSet.update({i.cand_id:[res.count(),i.ep_id_id]})

    resultDetail = resSet

    l = {}      #for storing won candidate of one panel at a time
    l1 = {}     # for storing won candidate of all panels
    for i in epanel_ids1:           # find won candidates
        max=-1
        for key,value in resSet.items():
            if value[1]==i:
                if max==-1:
                    max = value[0]
                    l.update({key:[max,i]})

                if max == value[0]:
                    l.update({key:[max,i]})
                elif max < value[0]:
                    l = {}
                    max = value[0]
                    l.update({key:[max,i]})
        l1.update(l)

    resSet = l1

    tie=0
    clist = []
    part=party.objects.filter(party_status=1)
    if part.count()>0:
        for p in part:
            clist.append(0)
        clist.append(0)
        le=len(clist)
        for key, value in resSet.items():
            cd=candidate.objects.get(cand_id=key)
            f = 0
            for k, v in resSet.items():
                cc=candidate.objects.get(cand_id=k)
                if key!=k:
                    if cc.ep_id_id==cd.ep_id_id:
                        f=1
                        break
            if f==1:
                tie=tie+1
                continue

            if cd.party_id_id!=None:
                b=0
                for p in part:
                    if p.party_id==cd.party_id_id:
                        clist[b]=clist[b]+1
                    b=b+1
            else:
                clist[le-1]= clist[le-1]+1

        if (candList):  # count for panels with only one candidate
            for a in candList:
                if a.party_id_id != None:
                    b = 0
                    for p in part:
                        if p.party_id == a.party_id_id:
                            clist[b] = clist[b] + 1
                        b = b + 1
                else:
                    clist[le - 1] = clist[le - 1] + 1

    ep = election_panel.objects.filter(elect_id_id=ele_id)  # Polling percentage
    eptemp = ep
    for a in eptemp:
        cc = candidate.objects.filter(Q(ep_id_id=a.ep_id) & Q(cand_status=1))
        if cc.count() == 1 or cc.count() == 0:
            ep = ep.filter(~Q(ep_id=a.ep_id))

    s = student.objects.filter(voter_status=1)
    s = s.filter(stud_end_date__gte=eobj.elect_date)

    per = []
    for a in ep:
        if a.panel_id.panel_type == 1:
            s = s.filter(stud_gender='F')

        pin = panel_specific.objects.filter(panel_id_id=a.panel_id_id)
        if pin.count() > 0:
            s = s.filter(stud_course_id_id__in=pin.values('course_id_id'))

        spp = list(s.values())
        data = []
        if a.panel_id.panel_year != 0:

            td = datetime.date.today().year
            for b in s:
                join_year = s.stud_start_date.year
                if ((td - join_year) + 1) == a.panel_year:
                    for i in range(len(spp)):
                        if spp[i]['stud_id'] == s.stud_id:
                            data.append(spp[i])
                            # del spp[i]
        else:
            data = spp
        vc = vote.objects.filter(ep_id_id=a.ep_id).count()
        # return HttpResponse((vc/len(data))*100)
        if len(data)!=0:
            p = (vc / len(data)) * 100
        else:
            p=0
        per.append(round(p, 2))


    tie = int(tie / 2)
    c = candidate.objects.all()
    e = election.objects.filter(elect_status=0)
    menuHide = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1
    return render(request, 'home/electResult.html', {'res': resSet, 'cand': c, 'eDate': eobj.elect_date, 'candList':candList, 'resDetail':resultDetail,'part':part,'clist':clist,'tie':tie,'menuHide':menuHide,'per':per,'ep':ep})




def percent(request):
    e = election.objects.filter(elect_status=0)
    if e.count() == 0:
        messages.success(request, "No active election")
        return redirect('http://127.0.0.1:8000/home/')

    if e[0].elect_date != datetime.date.today():
        messages.success(request, "Election date is "+str(e[0].elect_date))
        return redirect('http://127.0.0.1:8000/home/')


    ep = election_panel.objects.filter(elect_id_id =e[0].elect_id)
    eptemp = ep
    for a in eptemp:
        cc=candidate.objects.filter(Q(ep_id_id=a.ep_id) & Q(cand_status=1))
        if cc.count()==1 or  cc.count()==0:
            ep=ep.filter(~Q(ep_id=a.ep_id))


    s = student.objects.filter(voter_status=1)
    s = s.filter(stud_end_date__gt=datetime.date.today())

    per=[]
    for a in ep:
        if a.panel_id.panel_type == 1:
            s = s.filter(stud_gender='F')

        pin = panel_specific.objects.filter(panel_id_id=a.panel_id_id)
        if pin.count() > 0:
            s = s.filter(stud_course_id_id__in=pin.values('course_id_id'))

        spp = list(s.values())
        data = []
        if a.panel_id.panel_year != 0:

            td = datetime.date.today().year
            for b in s:
                join_year = s.stud_start_date.year
                if ((td - join_year) + 1) == a.panel_year:
                    for i in range(len(spp)):
                        if spp[i]['stud_id'] == s.stud_id:
                            data.append(spp[i])
                            # del spp[i]
        else:
            data=spp
        vc=vote.objects.filter(ep_id_id=a.ep_id).count()
        #return HttpResponse((vc/len(data))*100)
        p=(vc/len(data))*100
        per.append(round(p,2))
    return render(request, 'home/polingpercent.html',{'per':per,'ep':ep})

  
def resetPass(request):

    if request.method=='POST':
        uname = request.POST['uname']
        mail = request.POST['mail']
        loginObj = login.objects.filter(username=uname)
        if loginObj.count()==0:
            messages.success(request,"Incorrect Data")
        elif loginObj.count() ==1:
            obj = loginObj.get()
            request.session['uname'] = obj.username
            if obj.user_type == 1:
                userobj = staff.objects.get(staff_id=obj.user_id)
                if mail == userobj.staff_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")
            if obj.user_type == 2:
                userobj = department.objects.get(dept_id=obj.user_id)
                if mail == userobj.dept_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")
            if obj.user_type == 3:
                userobj = student.objects.get(stud_id=obj.user_id)
                if mail == userobj.stud_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")
            if obj.user_type == 4:
                userobj = party.objects.get(party_id=obj.user_id)
                if mail == userobj.party_email:
                    otp =OTPgenerator()
                    request.session['otp'] = otp
                    sendOtpToMAil(mail,otp)
                    messages.success(request, "OTP has been send to your mail")
                    return redirect('http://127.0.0.1:8000/home/confirmPassword')
                else:
                    messages.success(request, "Incorrect Data")

    e = election.objects.filter(elect_status=0)
    menuHide = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1
    return render(request,'home/resetPassword.html',{'menuHide':menuHide})


def confirmPass(request):
    keys = request.session.keys()
    if 'otp' not in keys:
        messages.success(request, "Session Expired!")
        return redirect('http://127.0.0.1:8000/home/login')

    if request.method=='POST':
        otp = request.session['otp']
        uotp = request.POST['otp']
        upwd = request.POST['pwd']
        upwd1 = request.POST['pwd1']

        if otp != uotp :
            messages.success(request, "Incorrect OTP!")
        if upwd != upwd1:
            messages.success(request, "Password not match")
        if otp == uotp and upwd == upwd1:
            uname = request.session['uname']
            login.objects.filter(username=uname).update(password=upwd)
            messages.success(request, "Password Changed")
            del request.session['otp']
            del request.session['uname']
            return redirect('http://127.0.0.1:8000/home/login')

    e = election.objects.filter(elect_status=0)
    menuHide = 0
    if e.count() == 0:
        menuHide = 1
    elif e[0].elect_date != datetime.date.today():
        menuHide = 1
    return render(request,'home/confirmPassword.html',{'menuHide':menuHide})


def OTPgenerator():
    digits_in_otp = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(digits_in_otp)
    for i in range(6):
        OTP += digits_in_otp[math.floor(random.random() * length)]

    print(OTP)
    return OTP

def sendOtpToMAil(mailAddr, otp):
    subject = 'College_Election - OTP for Staff RESET PASSWORD'
    message = 'Hello,\nYour One Time Password for changing password is \n' + str(otp)
    recepient = str(mailAddr)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)

def electDetails(request):

    e = election.objects.filter(elect_status=0)
    if e.count()>0:
        return render(request, 'home/electionDetails.html',{'e':e})

    return redirect('http://127.0.0.1:8000/home/')