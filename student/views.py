from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponse
from tables.models import *
import datetime
from django.db.models import Q
from django.contrib import messages
from django.http import JsonResponse
import math, random
from django.core import serializers
import cv2
import csv
import numpy as np
import pandas as pd
import os
from django.shortcuts import render



def getName(request):
    t_did = request.session['id']
    t_d = student.objects.get(stud_id=t_did)
    t_name = t_d.stud_fname + ' ' + t_d.stud_mname + ' ' + t_d.stud_lname
    return t_name

# Create your views here.
def home(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    """ check for valid stud """
    t_name = getName(request)

    sid = request.session['id']

    e = election.objects.filter(elect_status=0)

    if e.count() > 0:

        e = election.objects.get(elect_status=0)
        ep = election_panel.objects.filter(elect_id_id=e.elect_id).values('ep_id')

        c = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(cand_status=1) & Q(stud_id_id=sid))
        if c.count() > 0:
            return render(request, 'student/master.html',{'sym':1,'name':t_name})
    return render(request, 'student/master.html',{'name':t_name})


def personalinfo(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/student')

    sid = request.session['id']

    st = student.objects.filter(stud_id=sid, voter_status=1)
    if st.count() > 0:
        #messages.success(request, "You are already approved")
        #return redirect('http://127.0.0.1:8000/home/student')
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfo')

    sid = request.session['id']
    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')

    if request.method == 'POST' and request.FILES['photo']:
        phone = request.POST.get('mob')
        dob = request.POST.get('dob')
        photo = request.FILES.get('photo')
        student.objects.filter(stud_id=sid).update(stud_mob=phone, stud_photo=photo, stud_dob=dob, voter_status=0)
        s = student.objects.get(stud_id=sid)
        s.stud_photo = request.FILES['photo']
        s.save()
        messages.success(request, "Account activation requested.")
        return redirect('http://127.0.0.1:8000/home/student')
    t_name = getName(request)
    return render(request, 'student/PersonalInfo.html', {'s': s1,'name':t_name})


def personaledit(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    sid = request.session['id']
    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')
    s = student.objects.get(stud_id=sid)
    """if request.method == 'POST':
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        photo = request.FILES.get('photo')
        if mob != '':
            s.stud_temp_mob = mob
        if photo != '':
            s.stud_temp_photo = stud_photo = request.FILES['photo']
        s.save()
    """
    t_name = getName(request)
    return render(request, 'student/PersonalEdit.html', {'s': s,'name':t_name})


def otpverify(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')
    sid = request.session['id']


    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')


    secure = securevote.objects.filter(stud_id_id=sid)

    if secure.count()>0:  # check for blocked student
        if secure[0].remainingOtp == 0:
            messages.success(request, "Maximum number of retries reached. So you can't cast vote.")
            return redirect('http://127.0.0.1:8000/home/student')

    """check for active election on today with time from 9am to 1pm"""
    td = datetime.date.today()
    e = election.objects.filter(elect_status=0, elect_date=td)
    if e.count() > 0:
        t = datetime.datetime.now()
        if t.hour <= 8:
            messages.success(request, "Voting starts at 9am!")
            return redirect('http://127.0.0.1:8000/home/student')
        if t.hour > 12:
            messages.success(request, "Voting ends!")
            return redirect('http://127.0.0.1:8000/home/student')
    else:
        e = election.objects.filter(elect_status=0)
        if e.count()>0:
            messages.success(request, "Election date is "+ str(e[0].elect_date))
            return redirect('http://127.0.0.1:8000/home/student')
        else:
            messages.success(request, "Election Not Found")
            return redirect('http://127.0.0.1:8000/home/student')

    secure = securevote.objects.filter(stud_id_id=sid)
    if secure.count() == 0:
        secureObj = securevote(stud_id_id=sid)  # inital loading
        secureObj.save()
    if secure[0].initState == 2:  # otp verified for this section
        return redirect('http://127.0.0.1:8000/home/student/votingPanel')
    if request.method == 'POST':
        if 'sendOtp' in request.POST.keys() and secure[0].initState == 0:  # send otp
            securevote.objects.filter(stud_id_id=sid).update(initState=1)  # send otp done and wait for otp
            otpVal = OTPgenerator()
            print("OTP Generated")
            securevote.objects.filter(stud_id_id=sid).update(otp=otpVal)
            s = student.objects.filter(stud_id=sid)
            s = s.get();
            sendOtpToMAil(s.stud_email, otpVal)
            messages.success(request, "OTP has been sent to your mail.")
        elif 'formSubmit' in request.POST.keys() and secure[0].initState == 1:
            userOtp = request.POST['otp']
            if userOtp != secure[0].otp:
                if secure[0].remainingOtp == 3:
                    messages.success(request,
                                     "Incorrect OTP. Number of retries available is 2")
                    retry = secure[0].remainingOtp - 1
                    securevote.objects.filter(stud_id_id=sid).update(remainingOtp=retry)
                elif secure[0].remainingOtp == 2:
                    retry = secure[0].remainingOtp - 1
                    securevote.objects.filter(stud_id_id=sid).update(remainingOtp=retry)
                    messages.success(request, "Incorrect OTP. Number of retries available is 1")
                elif secure[0].remainingOtp == 1:
                    retry = secure[0].remainingOtp - 1
                    securevote.objects.filter(stud_id_id=sid).update(remainingOtp=retry)
                    messages.success(request, "Maximum number of retries reached. So you can't cast vote.")
                    return redirect('http://127.0.0.1:8000/home/student')


            else:
                securevote.objects.filter(stud_id_id=sid).update(initState=2)  # otp verified for this section
                return redirect('http://127.0.0.1:8000/home/student/votingPanel')

    t_name = getName(request)
    return render(request, 'student/Verify.html', {'initState': secure[0].initState,'name':t_name})


def nomination(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    sid = request.session['id']
    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')

    if request.method == 'POST':
        epid = request.POST.get('epid')
        sp1 = request.POST.get('sp1')
        sp2 = request.POST.get('sp2')
        ce = candidate.objects.filter(ep_id_id=epid, stud_id_id=sid)
        if ce.count() > 0:
            ce.update(cand_support_id1_id=sp1, cand_support_id2_id=sp2)
        else:
            cad = candidate(ep_id_id=epid, stud_id_id=sid, cand_support_id1_id=sp1, cand_support_id2_id=sp2,
                            accept_sts=1)
            cad.save()
        messages.success(request, "Nomination Submitted")
        return redirect('http://127.0.0.1:8000/home/student/')

    e = election.objects.filter(elect_status=0)

    if e.count() == 0:

        messages.success(request, "Election Not Found")
        return redirect('http://127.0.0.1:8000/home/student/')
    else:
        obj = election.objects.get(elect_status=0)
        nomStartDt = obj.elect_nomi_start_date
        nomEndDt = obj.elect_nomi_end_date
        today = datetime.date.today()

        if today < nomStartDt:
            messages.success(request, "Sorry! Nomination Receiving is not started")
            return redirect('http://127.0.0.1:8000/home/student/')

        if today > nomEndDt:
            messages.success(request, "Sorry! Nomination Receiving Date Over")
            return redirect('http://127.0.0.1:8000/home/student/')

    e = election.objects.get(elect_status=0)
    ep = election_panel.objects.filter(elect_id_id=e.elect_id)
    sc = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')) & Q(Q(cand_support_id1_id=sid) | Q(cand_support_id2_id=sid)))
    if sc.count() > 0:
        messages.success(request,"You cannot submit nomination because you either second a candidate already or a candidate choose you as their proposer ")
        return redirect('http://127.0.0.1:8000/home/student/')

    sp = student.objects.filter(~Q(stud_id=sid) & Q(voter_status=1))  # students other than login student and voter status=1
    # sp=None
    sp = sp.filter(stud_end_date__gt=datetime.date.today())
    # print(sp)
    cp = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')))  # election panel in current election

    if cp.count() > 0:
        # sp = student.objects.filter(~Q(stud_id=sid) & Q(voter_status=1))
        sp = sp.filter(~Q(stud_id__in=cp.values('stud_id_id')))
        cp = cp.filter(~Q(cand_support_id1_id=None), ~Q(cand_support_id2_id=None))
        if cp.count() > 0:
            sp = sp.filter(~Q(stud_id__in=cp.values('cand_support_id1_id')))
            sp = sp.filter(~Q(stud_id__in=cp.values('cand_support_id2_id')))

    # request.session['sps'] = list(sp.values())

    # return HttpResponse(sp)

    c = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')) & Q(stud_id_id=sid) & ~Q(cand_support_id1_id=None) & ~Q(cand_support_id2_id=None))
    if c.count() > 0:
        messages.success(request, "You already submitted a nomination")
        return redirect('http://127.0.0.1:8000/home/student/')

    s = student.objects.get(stud_id=sid)
    c = course.objects.get(course_id=s.stud_course_id_id)
    dep = department.objects.get(dept_id=c.dept_id_id)
    # return HttpResponse(d.dept_name)
    dob = s.stud_dob

    td = datetime.date.today()
    if td >= dob:
        age = td.year - dob.year
    else:
        age = (td.year - dob.year) - 1

    p = None
    pc = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')) & Q(stud_id_id=sid) & ~Q(party_id_id=None))
    # return HttpResponse(pc)

    data = []
    if pc.count() == 0:

        sp = None
        # data=[]
        p = panel.objects.filter(panel_status=1)
        if s.stud_gender == 'M':
            p = p.filter(Q(panel_type=0))
            sd = s.stud_start_date.year
            td = datetime.date.today().year
            d = (td - sd) + 1
            p = p.filter(Q(panel_year=0) | Q(panel_year=d))

        ps = panel_specific.objects.filter(Q(panel_id_id__in=p.values('panel_id')))
        if ps.count() > 0:
            pss=ps.filter(course_id_id=s.stud_course_id_id)
            if pss.count()>0:
                pout=ps.filter(~Q(panel_id_id__in=pss.values('panel_id_id')))
            else:
                pout=ps
            p = p.filter(~Q(panel_id__in=pout.values('panel_id_id')))
            #p = p.filter(~Q(panel_id__in=ps.values('panel_id_id')) | Q(panel_id__in=ps.filter(course_id_id=s.stud_course_id_id).values('panel_id_id')))
            ep = ep.filter(panel_id_id__in=p.values('panel_id'))
    else:
        pch = candidate.objects.get(Q(ep_id_id__in=ep.values('ep_id')) & Q(stud_id_id=sid) & ~Q(party_id_id=None))
        #pch = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')) & Q(stud_id_id=sid) & ~Q(party_id_id=None))
        if pch.accept_sts == 0:
            messages.success(request, "A party choose you as their candidate please respond to it")
            return redirect('http://127.0.0.1:8000/home/student/confirm')

        pcd = pc.get(stud_id_id=sid)
        elp = election_panel.objects.get(ep_id=pcd.ep_id_id)
        # return HttpResponse(elp)
        pan = panel.objects.get(panel_id=elp.panel_id_id)
        pans = panel_specific.objects.filter(panel_id_id=pan.panel_id)
        if pans.count() > 0:
            sp = sp.filter(stud_course_id_id__in=pans.values('course_id_id'))

        spp = list(sp.values())

        td = datetime.date.today().year
        py = pan.panel_year
        if py != 0:
            for s in sp:
                join_year = s.stud_start_date.year
                if ((td - join_year) + 1) == py:
                    for i in range(len(spp)):
                        if spp[i]['stud_id'] == s.stud_id:
                            data.append(spp[i])
                            # del spp[i]
        else:
            data = spp

        for a in pc:
            ep = ep.get(ep_id=a.ep_id_id)
            p = panel.objects.get(panel_id=ep.panel_id_id)

    next_year = e.elect_date.year + 1
    stud = student.objects.all()
    t_name = getName(request)
    return render(request, 'student/nomination.html',
                  {'data':data,'s': s, 'c': c, 'd': dep, 'age': age, 'e': e, 'p': p, 'ep': ep, 'pc': pc, 'sp': sp,
                   'next_year': next_year,'name':t_name})


def confirm(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    sid = request.session['id']

    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')

    e = election.objects.filter(elect_status=0)
    if e.count() == 0:
        messages.success(request, "No election declared")
        return redirect('http://127.0.0.1:8000/home/student')

    e = election.objects.filter(elect_status=0)

    if e.count() > 0:

        e = election.objects.get(elect_status=0)
        ep = election_panel.objects.filter(elect_id_id=e.elect_id).values('ep_id')

        c = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))

        if c.count() > 0:
            cd = candidate.objects.get(Q(ep_id_id__in=ep) & Q(Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))
            cs = student.objects.get(stud_id=cd.stud_id_id)

    if request.method == 'POST':
            e = election.objects.filter(elect_status=0)
            if e.count():
                e = election.objects.get(elect_status=0)
                ep = election_panel.objects.filter(elect_id_id=e.elect_id).values('ep_id')

            b = request.POST.get('btn')
            if b == 'paccept':
                party.objects.filter(support_id_id=sid).update(support_status=1)
            if b == 'preject':
                party.objects.filter(support_id_id=sid).update(support_status=None)

            if b == 'Caccept':
                candidate.objects.filter(Q(ep_id_id__in=ep) & Q(stud_id_id=sid) & ~Q(party_id_id=None) & Q(accept_sts=0)).update(accept_sts=1)
                # candidate.objects.filter(Q(stud_id_id=sid) & ~Q(party_id_id=None) & Q(accept_sts=0)).update(accept_sts=1)
            if b == 'Creject':
                # candidate.objects.get(Q(ep_id_id__in=ep) & Q(stud_id_id=sid) & ~Q(party_id_id=None) & Q(accept_sts=0)).delete()
                candidate.objects.get(Q(ep_id_id__in=ep) & Q(stud_id_id=sid) & ~Q(party_id_id=None) & Q(accept_sts=0)).delete()
            if b == 'Saccept':
                cd = candidate.objects.get(Q(ep_id_id__in=ep) & Q(Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))
                if cd.cand_support_id1_id == sid:
                    cd.support_id1_status = 1
                else:
                    cd.support_id2_status = 1
                cd.save()

            if b == 'Sreject':
                candidate.objects.get(Q(ep_id_id__in=ep) & Q(Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid,support_id2_status=0))).delete()
            messages.success(request, "Response Recorded")
            return redirect('http://127.0.0.1:8000/home/student/confirm/')

    # val=dict()
    p = party.objects.filter(Q(support_id_id=sid) & Q(support_status=0))

    par = None
    pp = None
    cs = None
    c = None
    ca = None

    e = election.objects.filter(elect_status=0)
    if e.count() > 0:
        e = election.objects.get(elect_status=0)
        ep = election_panel.objects.filter(elect_id_id=e.elect_id).values('ep_id')
        c = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(
            Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))

        if c.count() > 0:
            cd = candidate.objects.get(Q(ep_id_id__in=ep) & Q(Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))
            cs = student.objects.get(stud_id=cd.stud_id_id)

        c = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(
            Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))

        if c.count() > 0:
            cd = candidate.objects.get(Q(ep_id_id__in=ep) & Q(Q(cand_support_id1_id=sid, support_id1_status=0) | Q(cand_support_id2_id=sid, support_id2_status=0)))
            cs = student.objects.get(stud_id=cd.stud_id_id)

        ca = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(stud_id_id=sid) & ~Q(party_id_id=None) & Q(accept_sts=0))
        print(ca)
        if ca.count() > 0:
            for a in ca:
                par = party.objects.get(party_id=a.party_id_id)
                pp = panel.objects.get(panel_id=election_panel.objects.get(ep_id=a.ep_id_id).panel_id_id)

    if p or ca or c:
        t_name = getName(request)
        return render(request, 'student/confirm.html', {'ps': p, 'ca': ca, 'par': par, 'pp': pp, 'c': c, 'cs': cs,'name':t_name})
    else:
        messages.success(request, "Nothing to confirm")
        return redirect('http://127.0.0.1:8000/home/student/')


def propose1(request):
    sp1 = request.GET.get('spt')
    epid = request.GET.get('epid')
    print(request.session.keys())
    # sp2=request.session['sp1']
    # sp2s=list(sp2.filter(~Q(stud_id=sp1)).values())
    # sp2=list(sp2.values())
    std = student.objects.get(stud_id=sp1)
    stdpic = std.stud_photo.url
    cr = course.objects.get(course_id=std.stud_course_id_id)
    stdcr = cr.course_name
    d = department.objects.get(dept_id=cr.dept_id_id)
    stddept = d.dept_name

    sid = request.session['id']
    e = election.objects.get(elect_status=0)
    ep = election_panel.objects.filter(elect_id_id=e.elect_id)
    sp = student.objects.filter(
        ~Q(stud_id=sid) & Q(voter_status=1))  # students other than login student and voter status=1
    sp = sp.filter(stud_end_date__gt=datetime.date.today())
    print(sp)

    sp = sp.filter(~Q(stud_id=sp1))
    cp = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')))  # election panel in current election
    if cp.count() > 0:
        sp = sp.filter(~Q(stud_id__in=cp.values('stud_id_id')))
        cp = cp.filter(~Q(cand_support_id1_id=None), ~Q(cand_support_id2_id=None))
        if cp.count() > 0:
            sp = sp.filter(
                ~Q(stud_id__in=cp.values('cand_support_id1_id')) & ~Q(stud_id__in=cp.values('cand_support_id2_id')))

    epn = election_panel.objects.get(ep_id=epid)
    pal = panel.objects.get(panel_id=epn.panel_id_id)
    psc = panel_specific.objects.filter(panel_id_id=pal.panel_id)

    if psc.count() > 0:
        sp = sp.filter(stud_course_id_id__in=psc.values('course_id_id'))

    spp = list(sp.values())
    data = []
    td = datetime.date.today().year
    py = pal.panel_year
    if py != 0:

        for s in sp:
            join_year = s.stud_start_date.year
            if ((td - join_year) + 1) == py:
                for i in range(len(spp)):
                    if spp[i]['stud_id'] == s.stud_id:
                        data.append(spp[i])
                        # del spp[i]
    else:
        data = spp

    if len(data) > 0:
        sd = [stdpic, stdcr, stddept, data]
    else:
        sd = [stdpic, stdcr, stddept]
    return JsonResponse(sd, safe=False)


def propose2(request):
    sp2 = request.GET.get('spt')

    print(request.session.keys())
    # sp2=request.session['sp1']
    # sp2s=list(sp2.filter(~Q(stud_id=sp1)).values())
    # sp2=list(sp2.values())
    std = student.objects.get(stud_id=sp2)
    stdpic = std.stud_photo.url
    cr = course.objects.get(course_id=std.stud_course_id_id)
    stdcr = cr.course_name
    d = department.objects.get(dept_id=cr.dept_id_id)
    stddept = d.dept_name
    sd = [stdpic, stdcr, stddept]
    return JsonResponse(sd, safe=False)


def panelselect(request):
    epid = request.GET.get('epid')

    sid = request.session['id']
    e = election.objects.get(elect_status=0)
    ep = election_panel.objects.filter(elect_id_id=e.elect_id)
    sp = student.objects.filter(
        ~Q(stud_id=sid) & Q(voter_status=1))  # students other than login student and voter status=1
    sp = sp.filter(stud_end_date__gt=datetime.date.today())
    cp = candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')))  # election panel in current election
    if cp.count() > 0:
        sp = sp.filter(~Q(stud_id__in=cp.values('stud_id_id')))
        cp = cp.filter(~Q(cand_support_id1_id=None), ~Q(cand_support_id2_id=None))
        if cp.count() > 0:
            sp = sp.filter(
                ~Q(stud_id__in=cp.values('cand_support_id1_id')) & ~Q(stud_id__in=cp.values('cand_support_id2_id')))

    epn = election_panel.objects.get(ep_id=epid)
    pal = panel.objects.get(panel_id=epn.panel_id_id)
    psc = panel_specific.objects.filter(panel_id_id=pal.panel_id)

    if psc.count() > 0:
        sp = sp.filter(stud_course_id_id__in=psc.values('course_id_id'))

    spp = list(sp.values())
    data = []
    td = datetime.date.today().year
    py = pal.panel_year
    if py != 0:

        for s in sp:
            join_year = s.stud_start_date.year
            if ((td - join_year) + 1) == py:
                for i in range(len(spp)):
                    if spp[i]['stud_id'] == s.stud_id:
                        data.append(spp[i])
                        # del spp[i]
    else:
        data = spp

    # data=
    return JsonResponse(data, safe=False)


def OTPgenerator():
    digits_in_otp = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    OTP = ""
    length = len(digits_in_otp)
    for i in range(6):
        OTP += digits_in_otp[math.floor(random.random() * length)]

    print(OTP)

    return OTP


def sendOtpToMAil(mailAddr, otp):
    subject = 'College_Election - OTP for Voting'
    message = 'Hello,\nYour One Time Password for voting is \n'+ str(otp)
    recepient = str(mailAddr)
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)


def epanel(request):  # voting view

    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')
    sid = request.session['id']

    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')


    if request.method == 'POST':
        print(request.POST)
        if 'nota' in request.POST.keys():
            vv = vote.objects.filter(ep_id_id=request.POST['nota'], stud_id_id=request.session['id'])
            if vv.count() == 0:
                obj = vote(ep_id_id=request.POST['nota'], stud_id_id=request.session['id'])
                obj.save()
        elif 'vote' in request.POST.keys():
            candid = int(request.POST['vote'])
            c = candidate.objects.get(cand_id=candid)
            vv = vote.objects.filter(ep_id_id=c.ep_id_id, stud_id_id=request.session['id'])
            if vv.count() == 0:
                obj = vote(ep_id_id=c.ep_id_id, stud_id_id=request.session['id'])
                obj.save()
                obj = result(ep_id_id=c.ep_id_id, cand_id_id=candid)
                obj.save()
        elif 'voteCheck' in request.POST.keys():
            candIds = request.POST.getlist('voteCheck')
            obj = election_panel.objects.get(ep_id=request.POST['moreVotes'])
            max_votes_panel = obj.panel_id.panel_votes
            vv = vote.objects.filter(ep_id_id=request.POST['moreVotes'], stud_id_id=request.session['id'])
            if vv.count() == 0:
                if len(candIds) == 0:
                    temp_flag = 1
                    messages.success(request, "Make atleast one vote or click on NOTA")
                elif len(candIds) <= max_votes_panel:
                    obj = vote(ep_id_id=request.POST['moreVotes'], stud_id_id=request.session['id'])
                    obj.save()

                    for id in candIds:
                        obj = result(ep_id_id=request.POST['moreVotes'], cand_id_id=id)
                        obj.save()

                else:
                    messages.success(request, "Maximum number of votes for this panel is " + str(max_votes_panel))

    e=election.objects.get(elect_status=0)
    epal=election_panel.objects.filter(elect_id_id=e.elect_id)
    s=student.objects.get(stud_id=sid)

    print("ELECTION ID "+str(e.elect_id))    
    if s.stud_gender=='M':
        epal=epal.filter(Q(panel_id_id__in=panel.objects.filter(panel_type=0).values('panel_id')))


    ps=panel_specific.objects.filter(Q(panel_id_id__in=epal.values('panel_id_id')))
    if ps.count()>0:
        pin=ps.filter(Q(course_id_id=s.stud_course_id_id))
        if pin.count()>0:
            pout=ps.filter(~Q(panel_id_id__in=pin.values('panel_id_id')))
        else:
            pout=ps
        epal=epal.filter(~Q(panel_id_id__in=pout.values('panel_id_id')))



    #return HttpResponse(epal)
    start=s.stud_start_date.year
    td=datetime.date.today().year
    stud_year=(td-start)+1
    epal=epal.filter(Q(panel_id__in=panel.objects.filter(Q(panel_year=0) | Q(panel_year=stud_year)).values('panel_id')))
    epal=epal.filter(~Q(ep_id__in=vote.objects.filter(stud_id_id=sid).values('ep_id_id')))

    eptemp=epal
    for a in eptemp:
        print("ELECTION_PANEL ID:"+str(a.ep_id)+" stud id "+str(sid))

    eptemp=epal
    for a in eptemp:
        cc=candidate.objects.filter(Q(ep_id_id=a.ep_id) & Q(cand_status=1))
        print("CC COUNT "+str(cc.count())+" Votes "+str(a.panel_id.panel_votes))
        if cc.count()<=a.panel_id.panel_votes:
            epal=epal.filter(~Q(ep_id=a.ep_id))
            print("ELECTION_PANEL ID:"+str(a.ep_id)+" cc count "+str(cc.count()))
            
    print(str(epal.count())+" EPANEL COUNT")
   # return HttpResponse(epal)ep
    if epal.count()>0:
        #return HttpResponse(epal)
        cand=candidate.objects.filter(Q(ep_id_id__in=epal.values('ep_id')) & Q(cand_status=1))
        #return HttpResponse(cand)
        if cand.count()==0:
            messages.success(request, "Voting Process Completed!")
            return redirect('http://127.0.0.1:8000/home/student/')

        cand = candidate.objects.filter(Q(ep_id_id=epal[0].ep_id) & Q(cand_status=1))
        epid=election_panel.objects.get(ep_id=cand[0].ep_id_id)
        post=panel.objects.get(panel_id=epid.panel_id_id).panel_post
        t_name = getName(request)
        return render(request, 'student/votingPanel.html', {'cand': cand, 'post': post,'name':t_name})
    else:
        messages.success(request, "Voting Process Completed")
        return redirect('http://127.0.0.1:8000/home/student/')


def nomwithdraw(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    sid = request.session['id']
    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')

    if request.method == 'POST':
        cdid = request.POST.get('withdraw')
        candidate.objects.filter(cand_id=cdid).update(withdraw_status=1)
        messages.success(request, "Nomination withdraw request submitted ")
        return redirect('http://127.0.0.1:8000/home/student')

    e = election.objects.filter(elect_status=0)
    if e.count() == 0:
        messages.success(request, "No election declared")
        return redirect('http://127.0.0.1:8000/home/student')

    ep = election_panel.objects.filter(elect_id_id=e[0].elect_id)
    cc = candidate.objects.filter(Q(stud_id_id=sid) & Q(ep_id_id__in=ep.values('ep_id')))
    if cc.count() == 0:
        messages.success(request, "No nomination submitted or nomination rejected")
        return redirect('http://127.0.0.1:8000/home/student')

    if cc[0].cand_support_id1_id == None and cc[0].cand_support_id2_id == None:
        messages.success(request, "Nomination is not submmitted")
        return redirect('http://127.0.0.1:8000/home/student')

    if cc[0].cand_status == 0:
        messages.success(request, "Nomination is not approved yet")
        return redirect('http://127.0.0.1:8000/home/student')

    if cc[0].withdraw_status == 1:
        messages.success(request, "You already submit withdrawal request")
        return redirect('http://127.0.0.1:8000/home/student')

    cid = cc[0].cand_id
    cd = candidate.objects.get(cand_id=cid)
    pal = panel.objects.get(panel_id=election_panel.objects.get(ep_id=cd.ep_id_id).panel_id_id)
    sd = student.objects.get(stud_id=cd.stud_id_id)
    dyear = sd.stud_dob
    if dyear >= datetime.date.today():
        a = (datetime.date.today().year - dyear.year)
    else:
        a = (datetime.date.today().year - dyear.year) - 1

    canc = course.objects.get(course_id=sd.stud_course_id_id)
    cand = department.objects.get(dept_id=canc.dept_id_id)

    spd1 = student.objects.get(stud_id=cd.cand_support_id1_id)
    spd2 = student.objects.get(stud_id=cd.cand_support_id2_id)
    spd1c = course.objects.get(course_id=spd1.stud_course_id_id)
    spd2c = course.objects.get(course_id=spd2.stud_course_id_id)
    spd1d = department.objects.get(dept_id=spd1c.dept_id_id)
    spd2d = department.objects.get(dept_id=spd2c.dept_id_id)

    t_name = getName(request)
    return render(request, 'student/nomwithdraw.html',
                  {'cc': cd, 'p': pal, 'sd': sd, 'age': a, 'canc': canc, 'cand': cand, 'spd1': spd1, 'spd2': spd2,
                   'spd1c': spd1c, 'spd2c': spd2c, 'spd1d': spd1d, 'spd2d': spd2d,'name':t_name})


def mysymbol(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    sid = request.session['id']
    s1 = student.objects.filter(stud_id=sid)
    s1 = s1.get()
    if s1.voter_status == 0:
        messages.success(request, "Account not verified yet! Once verified, you will get an email. Thank You")
        return redirect('http://127.0.0.1:8000/home/student')
    elif s1.voter_status == None:
        messages.success(request, "Account not activated.")
        return redirect('http://127.0.0.1:8000/home/student/PersonalInfoAdd')

    e = election.objects.filter(elect_status=0)

    if e.count() > 0:

        e = election.objects.get(elect_status=0)
        ep = election_panel.objects.filter(elect_id_id=e.elect_id).values('ep_id')

        c = candidate.objects.filter(Q(ep_id_id__in=ep) & Q(cand_status=1) & Q(stud_id_id=sid))
        if c.count() > 0:
            t_name = getName(request)
            return render(request, 'student/mySymbol.html',{'sym':c[0].symbol_id.symbol_loc.url,'e':e,'name':t_name})

    return redirect('http://127.0.0.1:8000/home/student/')
