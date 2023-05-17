import datetime
from django.shortcuts import render,redirect
from tables.models import *
from django.db.models import Q, Count
from django.http import HttpResponse
from django.contrib import messages
#for email
import datetime
from College_Election.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
#for ajax response
from django.http import  JsonResponse, HttpResponseRedirect
# Create your views here.
def home(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    return render(request,'administrator/master.html')

def paneladd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    e=election.objects.filter(elect_status=0)
    if e.count()>0:
        messages.success(request, "Cannot add panel, because an election is declared")
        return redirect('http://127.0.0.1:8000/home/admin')


    cs=course.objects.all()
    if request.method=='POST':
        pname=request.POST.get('pname')
        ptype=int(request.POST.get('ptype'))
        #pstatus=int(request.POST.get('pstatus'))
        yob=int(request.POST.get('yob'))
        cr=request.POST.getlist('checks')
        p=panel(panel_post=pname,panel_type=ptype,panel_year=yob)
        p.save()
        if len(cr)>0:
            for c in cr:
                ps=panel_specific(course_id_id=c,panel_id_id=p.panel_id)
                ps.save()

        messages.success(request, "Panel Details Saved Successfully")
    obj = panel.objects.all()
    if obj.count()==0:
        return render(request,'administrator/paneladd.html',{'courses':cs})
    return render(request, 'administrator/paneladd.html', {'courses': cs,'d':obj})

def paneledit(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    p = panel.objects.all()
    if p.count()==0:
        messages.success(request, "Panels not found!")
        return redirect('http://127.0.0.1:8000/home/admin')

    e = election.objects.filter(elect_status=0)
    if e.count() > 0:
        messages.success(request, "Cannot add panel, because an election is declared")
        return redirect('http://127.0.0.1:8000/home/admin')

    p = panel.objects.all()
    p_s = panel_specific.objects.all()
    c = course.objects.all()
    p_s_id = []
    c_id = []
    for c1 in c:
        c_id.append(c1.course_id)
    for s1 in p_s:
        p_s_id.append(s1.panel_id.panel_id) #id's of panel in panel_specific
    if request.method=='POST':
        panelid = request.POST.get('approve')
        ptype = int(request.POST.get('ptype'+str(panelid)))
        yob = int(request.POST.get('yob'+str(panelid)))
        cr = request.POST.getlist('checks'+str(panelid))

        if len(cr)==0:
            if int(panelid) in p_s_id:   #delete all entries of panel from panel_specific
                obj = panel_specific.objects.filter(panel_id=panelid).delete()
        else:
            obj = panel_specific.objects.filter(panel_id=panelid).delete()
            for c1 in cr:
                ps=panel_specific(course_id_id=c1,panel_id_id=panelid)
                ps.save()
        obj = panel.objects.filter(panel_id=panelid).update(panel_type=ptype,panel_year=yob)

        messages.success(request, "Panel Details Edited Successfully")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return render(request,'administrator/paneledit.html', {'p':p,'p_s':p_s, 'c':c})

def deptadd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    e = election.objects.filter(elect_status=0)
    if e.count() > 0:
        messages.success(request, "Cannot add panel, because an election is declared")
        return redirect('http://127.0.0.1:8000/home/admin')


    if request.method=='POST':
        dname = request.POST.get('dname')
        dmail = request.POST.get('dmail')
        dphone = request.POST.get('txtPhone')
        s = department.objects.filter(dept_name=dname)
        dname_status= dmail_status = False
        if s.count() > 0:
            dname_status = True
        s = department.objects.filter(dept_email=dmail)
        if s.count() > 0:
            dmail_status = True
        if not(dmail_status) or not(dname_status):
            d=department(dept_name=dname,dept_email=dmail,dept_phone=dphone)
            d.save()
            user="dept"+str(d.dept_id)
            pwd="dept"+str(d.dept_id)
            l=login(username=user,password=pwd,user_type=2,user_id=d.dept_id)
            l.save()
            #send username and password to mail
            subject = 'College_Election - '+dname+' Department Login Details'
            message = 'Hello,\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: '+user+'\nPassword: '+pwd
            message += '\nNote: Please use forgot password option to change your password!'
            recepient = str(dmail)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            messages.success(request,"Department Registration Success")
        else:
            messages.success(request, "Data Repetition Found!")
    obj = department.objects.all()
    if obj.count() ==0:
        return render(request,'administrator/deptadd.html')

    return render(request, 'administrator/deptadd.html',{'d':obj})

def electionadd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    e=election.objects.filter(elect_status=0)
    if e.count()>0:
        messages.success(request, "Currently an Active Election Exists!")
        return redirect('http://127.0.0.1:8000/home/admin')

    pls=panel.objects.all()
    if pls.count()==0:
        messages.success(request, "Panels not added!")
        return redirect('http://127.0.0.1:8000/home/admin')


    if request.method=='POST':
        nomStartDt=request.POST.get('nomStartDt')
        nomEndDt=request.POST.get('nomEndDt')
        nomWithDt=request.POST.get('nomWithDt')
        electDt=request.POST.get('electDt')
        ps=request.POST.getlist('panels')

        e=election(elect_date=electDt,elect_nomi_end_date=nomEndDt,elect_nomi_start_date=nomStartDt,elect_nomi_withdrawal_end_date=nomWithDt)
        e.save()
        if len(ps):
            for a in ps:
                es=election_panel(elect_id_id=e.elect_id,panel_id_id=a)
                es.save()
        else:
            pal = panel.objects.all()
            for a in pal:
                es = election_panel(elect_id_id=e.elect_id, panel_id_id=a.panel_id)
                es.save()





        #p=panel.objects.filter(panel_status=1)
        #for a in p:
            #es=election_panel(elect_id_id=e.elect_id,panel_id_id=a.panel_id)
            #es.save()
        messages.success(request,"Election Details Saved")
        return redirect('http://127.0.0.1:8000/home/admin')

    p=panel.objects.all()

    s = student.objects.filter(voter_status=0)
    count = 0
    for i in s:
        if datetime.date.today() <= i.stud_end_date:
            count += 1
    if count > 0:
        return render(request, 'administrator/electionadd.html', {'p': p,'count':count})
    return render(request,'administrator/electionadd.html',{'p':p})

def staffadd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    if request.method=='POST':
        fname = request.POST.get('fname')
        mname = request.POST.get('mname')
        lname = request.POST.get('lname')
        email = request.POST.get('dmail')
        phone = request.POST.get('txtPhone')
        s = staff.objects.filter(staff_email=email)
        if s.count() == 0:
            st=staff(staff_fname=fname,staff_mname=mname,staff_lname=lname,staff_email=email,staff_phone=phone,staff_status=1)
            st.save()
            user = "staff" + str(st.staff_id)
            pwd = "staff" + str(st.staff_id)
            l = login(username=user, password=pwd, user_type=1, user_id=st.staff_id)
            l.save()
            # send username and password to mail
            subject = 'College_Election - ' + fname +' ' + mname + ' ' + lname + ' Staff Login Details'
            message = 'Hello,\nYour login credentials for http://127.0.0.1:800/home are as follows,\nUsername: ' + user + '\nPassword: ' + pwd
            message += '\nNote: Please use forgot password option to change your password!'
            recepient = str(email)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            messages.success(request, "Staff Registration Success")
        else:
            messages.success(request, "Email Already Exist!")

    return render(request,'administrator/staffadd.html')

def nomapprove(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')
    print(keys)
    if request.method=='POST':
        print(request.POST)
        if request.POST.get('Accept'):
            ac=request.POST.get('Accept')
            print(ac)
            ep = election.objects.all().last()
            c1 = candidate.objects.filter(ep_id__in=election_panel.objects.filter(elect_id=ep)).filter(~Q(symbol_id_id=None))
            s = symbol.objects.all()
            candidate.objects.filter(cand_id=ac).update(cand_status=1,symbol_id=None)
            messages.success(request, "Nomination approved")
            s_list = []
            for i in s:
                s_list.append(i.symbol_id)
            for i in c1:
                if i.symbol_id_id in s_list:
                    s_list.remove(i.symbol_id_id)
            sym = symbol.objects.filter(symbol_id__in=s_list)
            #sym=symbol.objects.all()
            # if sym.count()==0:
            #     print("syscount zero")
            #     messages.success(request, "No symbol available for this panel,please add symbol")
            #     print("No symbol available for this panel,please add symbol")
            #     return redirect('http://127.0.0.1:8000/home/admin')
            # else:
            #     print("symcount not zero000")
            #     return render(request,'administrator/symbolalloc.html',{'sym':sym,'cand':ac})
            print("Nomination approved")

            # candidate.objects.filter(cand_id=ac).update(cand_status=1,symbol_id=sb)
            # messages.success(request, "Nomination approved")
        elif request.POST.get('Reject'):
            # rj = request.POST.get('Reject')
            c=candidate.objects.get(cand_id=rj)
            subject = 'Nomination Result'
            message = '\nDear ' + c.stud_id.stud_fname +' '+ c.stud_id.stud_mname+' '+c.stud_id.stud_lname+ '\n Your nomination is rejected'
            recepient = str(c.stud_id.stud_email)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            candidate.objects.filter(cand_id=rj).delete()
            messages.success(request, "Nomination rejected")

        elif request.POST.get('view'):
            cid=request.POST.get('view')
            cd=candidate.objects.get(cand_id=cid)
            pal=panel.objects.get(panel_id=election_panel.objects.get(ep_id=cd.ep_id_id).panel_id_id )
            sd=student.objects.get(stud_id=cd.stud_id_id)
            dyear=sd.stud_dob
            if dyear>=datetime.date.today():
                a=(datetime.date.today().year-dyear.year)
            else:
                a = (datetime.date.today().year - dyear.year)-1

            canc = course.objects.get(course_id=sd.stud_course_id_id)
            cand = department.objects.get(dept_id=canc.dept_id_id)
            spd1 = student.objects.get(stud_id=cd.cand_support_id1_id )
            spd2 = student.objects.get(stud_id=cd.cand_support_id2_id)
            spd1c = course.objects.get(course_id=spd1.stud_course_id_id)
            spd2c = course.objects.get(course_id=spd2.stud_course_id_id)
            spd1d=department.objects.get(dept_id=spd1c.dept_id_id)
            spd2d = department.objects.get(dept_id=spd2c.dept_id_id)

            e = election.objects.get(elect_status=0)
            next_year = e.elect_date.year + 1

            return render(request, 'administrator/nompaper.html',{'p':pal,'sd':sd,'age':a,'canc':canc,'cand':cand,'spd1':spd1,'spd2':spd2,'spd1c':spd1c,'spd2c':spd2c,'spd1d':spd1d,'spd2d':spd2d, 'curyear':e.elect_date.year,'nextyear':next_year})
        else:
            print("s")
            candid=request.POST.get('NomFinal')
            c = candidate.objects.get(cand_id=candid)
            subject = 'Nomination Result'
            message = '\nDear ' + c.stud_id.stud_fname + ' ' + c.stud_id.stud_mname + ' ' + c.stud_id.stud_lname + '\n You nomination is approved'
            recepient = str(c.stud_id.stud_email)
            print(message)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            sym=request.POST.get('symb')
            candidate.objects.filter(cand_id=candid).update(cand_status=1, symbol_id=sym)
            messages.success(request, "Nomination Approved")
            #return redirect('http://127.0.0.1:8000/home/admin/nomapprove')

    e=election.objects.filter(elect_status=0)
    if e.count()==0:
        messages.success(request, "Election Not Declared!")
        return redirect('http://127.0.0.1:8000/home/admin')

    td = datetime.date.today()
    obj = election.objects.get(elect_status=0)
    electDate = obj.elect_date
    if td >= electDate:
        messages.success(request, "Time for Nomination Approval over!")
        return redirect('http://127.0.0.1:8000/home/admin')

    e = election.objects.get(elect_status=0)
    ep=election_panel.objects.filter(elect_id_id=e.elect_id)
    cds=candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')) & ~Q(cand_support_id1_id=None) & ~Q(cand_support_id2_id=None) & Q(support_id1_status=1) & Q(support_id2_status=1) & Q(cand_status=0))

    if cds.count()==0:
        messages.success(request, "Nomination not found for approval!")
        return redirect('http://127.0.0.1:8000/home/admin')

    ep=ep.filter(ep_id__in=cds.values('ep_id_id'))
    p = panel.objects.filter(panel_id__in=ep.values('panel_id_id'))
    pt=party.objects.all()
    s=student.objects.filter(stud_id__in=cds.values('stud_id_id'))

    #return HttpResponse(p)
    symb=symbol.objects.all()
    return render(request,'administrator/nomapprove.html',{'cds':cds,'ep':ep,'p':p,'stud':s,'pt':pt,'symb':symb})

def nompaper(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    return render(request,'administrator/nompaper.html')

def symboladd(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    if request.method=='POST' and request.FILES['symbol']:
        myfile = request.FILES.get('symbol')
        s = symbol(symbol_loc=myfile)
        s.save()
        sym = symbol.objects.all()
        return render(request, 'administrator/symboladd.html', {'myfile_url': s, 'sym' : sym})
    sym = symbol.objects.all()
    return render(request,'administrator/symboladd.html', {'sym':sym})

def partyapprove(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    if request.method=='POST':
        pid=request.POST.get('approve')
        party.objects.filter(party_id=pid).update(party_status=1)
        p=party.objects.get(party_id=pid)
        subject = 'Success-Party Registration'
        message = '\nDear '+p.party_name+'\n You are approved'
        recepient = str(p.party_email)
        send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
        messages.success(request, "Student Organization Approved Successfully")

    p=party.objects.filter(Q(party_status=0) & Q(support_status=1))
    if p:
        c=course.objects.all()
        d=department.objects.all()
        s=student.objects.all()
        return render(request,'administrator/partyapprove.html',{'party':p,'course':c,'dept':d,'stud':s})
    else:
        messages.success(request, "Pending Approvals Not Found")
        return redirect('http://127.0.0.1:8000/home/admin/')

def validate_dept(request):
    dname = request.GET.get('dname')
    dmail = request.GET.get('dmail')
    s = department.objects.filter(dept_name=dname)
    dname_status = False
    dmail_status = False
    if s.count() > 0:
        dname_status =True
    s = department.objects.filter(dept_email=dmail)
    if s.count() > 0:
        dmail_status = True
    data = {
        'dname_status' :dname_status,
        'dmail_status' :dmail_status
    }
    return JsonResponse(data)

def validate_staff(request):
    dmail = request.GET.get('dmail')
    s = staff.objects.filter(staff_email=dmail)
    staffmail_status = False
    if s.count() > 0:
        staffmail_status = True
    data = {
        'dmail_status': staffmail_status
    }
    return JsonResponse(data)


def withdrawapprove(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    if request.method=='POST':

        if request.POST.get('Approve'):
            candid=request.POST.get('Approve')
            c = candidate.objects.get(cand_id=candid)
            subject = 'Nomination Withdraw Request Result'
            message = '\nDear ' + c.stud_id.stud_fname + ' ' + c.stud_id.stud_mname + ' ' + c.stud_id.stud_mname + '\n Your request for nomination withdrawal is approved'
            recepient = str(c.stud_id.stud_email)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            candidate.objects.filter(cand_id=candid).delete()
            messages.success(request, "Nomination Rejected")
            return redirect('http://127.0.0.1:8000/home/admin')
        else:
            candid = request.POST.get('Reject')
            c = candidate.objects.get(cand_id=candid)
            subject = 'Nomination Withdraw Request Result'
            message = '\nDear ' + c.stud_id.stud_fname + ' ' + c.stud_id.stud_mname + ' ' + c.stud_id.stud_mname + '\n Your request for nomination withdrawal is rejected '
            recepient = str(c.stud_id.stud_email)
            send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently=False)
            candidate.objects.filter(cand_id=candid).update(withdraw_status=0)
            messages.success(request, "Nomination Rejected")
            return redirect('http://127.0.0.1:8000/home/admin')




    e=election.objects.filter(elect_status=0)
    if e.count()==0:
        messages.success(request, "No election declared")
        return redirect('http://127.0.0.1:8000/home/admin')


    ep=election_panel.objects.filter(elect_id_id=e[0].elect_id)
    #return  HttpResponse(ep)
    cd=candidate.objects.filter(Q(ep_id_id__in=ep.values('ep_id')) & Q(withdraw_status=1))
    if cd.count()==0:
        messages.success(request, "No withdraw request to verify")
        return redirect('http://127.0.0.1:8000/home/admin')

    s=student.objects.all()
    c=course.objects.all()
    d=department.objects.all()
    pt=party.objects.all()
    ep=election_panel.objects.all()
    p=panel.objects.all()
    symb=symbol.objects.all()
    return render(request, 'administrator/withdrawapprove.html', {'cds':cd,'stud':s,'pt':pt,'ep':ep,'p':p,'symb':symb})


def voteResult(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    e = election.objects.filter(elect_status=0)
    if e.count()==0:
        messages.success(request, "Election Not Found")
        return redirect('http://127.0.0.1:8000/home/admin')
    else:
        td = datetime.date.today()
        if td < e[0].elect_date :
            messages.success(request, "Election date is "+str(e[0].elect_date))
            return redirect('http://127.0.0.1:8000/home/admin')
        t = datetime.datetime.now()
        if t.hour<=8:
            messages.success(request, "Voting starts at 9am!")
            return redirect('http://127.0.0.1:8000/home/admin')
        if t.hour<=12:
            messages.success(request, "Voting ends at 1pm!")
            return redirect('http://127.0.0.1:8000/home/admin')

    if request.method == 'POST':
        e = election.objects.filter(elect_status=0).update(elect_status=1)
        securevote.objects.all().delete()
        return redirect('http://127.0.0.1:8000/home/admin/publish/')

    e = election.objects.filter(elect_status=0)
    #return HttpResponse(e.count())
    if e.count() == 0:
        messages.success(request, "Election Not Found")
        return redirect('http://127.0.0.1:8000/home/admin/')
    else:
        return render(request, 'administrator/resultPublish.html',{'eDate':e[0].elect_date, 'eId':e[0].elect_id})

def publishRes(request):

    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    e = election.objects.filter(elect_status=1)
    if e.count() == 0:
        messages.success(request, "Election Not Found")
        return redirect('http://127.0.0.1:8000/home/admin')

    eobj = election.objects.filter(elect_status=1).last()

    if request.method=='POST':
        eid = request.POST['eDate']
        eobj = election.objects.get(elect_id=eid)

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

    resSet = {}

    for i in candList1:  # votes counting
        res = result.objects.filter(cand_id=i)
        resSet.update({i.cand_id: [res.count(), i.ep_id_id]})

    resultDetail = resSet

    l = {}  # for storing won candidate of one panel at a time
    l1 = {}  # for storing won candidate of all panels
    for i in epanel_ids1:  # find won candidates
        max = -1
        for key, value in resSet.items():
            if value[1] == i:
                if max == -1:
                    max = value[0]
                    l.update({key: [max, i]})

                if max == value[0]:
                    l.update({key: [max, i]})
                elif max < value[0]:
                    l = {}
                    max = value[0]
                    l.update({key: [max, i]})
        l1.update(l)
    resSet = l1
    tie=0
    clist = []
    part = party.objects.filter(party_status=1)
    if part.count() > 0:
        for p in part:
            clist.append(0)
        clist.append(0)
        le = len(clist)
        for key, value in resSet.items():
            cd = candidate.objects.get(cand_id=key)
            f = 0
            for k, v in resSet.items():
                cc = candidate.objects.get(cand_id=k)
                if key != k:
                    if cc.ep_id_id == cd.ep_id_id:
                        #print('tie')
                        f = 1
                        break
            if f == 1:
                tie=tie+1
                continue
            if cd.party_id_id != None:
                b = 0
                for p in part:
                    if p.party_id == cd.party_id_id:
                        clist[b] = clist[b] + 1
                    b = b + 1
            else:
                clist[le - 1] = clist[le - 1] + 1




        if (candList):#count for panels with only one candidate
            for a in candList:
                if a.party_id_id!=None:
                    b = 0
                    for p in part:
                        if p.party_id == a.party_id_id:
                            clist[b] = clist[b] + 1
                        b = b + 1
                else:
                    clist[le - 1] = clist[le - 1] + 1

    ep = election_panel.objects.filter(elect_id_id=ele_id)#Polling percentage
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





    tie=int(tie/2)

    c = candidate.objects.all()

    return render(request, 'administrator/publish.html',
                  {'res': resSet, 'cand': c, 'eDate': eobj.elect_date, 'candList': candList, 'resDetail': resultDetail, 'e':e,'part':part,'clist':clist,'tie':tie,'per':per,'ep':ep})


def deptReport(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = department.objects.all()
    c = course.objects.all()
    if obj.count()==0:
        messages.success(request, "Department list is empty!")
        return redirect('http://127.0.0.1:8000/home/admin')

    return render(request, 'administrator/deptrpt.html',{'dept': obj, 'c': c})


def staffReport(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')
    obj = staff.objects.all()

    if obj.count() == 0:
        messages.success(request, "Staff list is empty!")
        return redirect('http://127.0.0.1:8000/home/admin')

    return render(request, 'administrator/staffrpt.html', {'staff':obj})


def partyReport(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = party.objects.all()

    if obj.count()==0:
        messages.success(request, "Organization list is empty!")
        return redirect('http://127.0.0.1:8000/home/admin')

    return render(request, 'administrator/partyrpt.html',{'p':obj})


def staffModify(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')

    obj = staff.objects.all()
    if obj.count()==0:
        messages.success(request, "Staff list is empty!")
        return redirect('http://127.0.0.1:8000/home/admin')

    if request.method=='POST':
        if 'active' in request.POST.keys():
            id = request.POST['active']
            staff.objects.filter(staff_id=id).update(staff_status=1)
        else:
            id = request.POST['inactive']
            staff.objects.filter(staff_id=id).update(staff_status=0)


    return render(request, 'administrator/staffModify.html', {'staff':obj})

def postpone(request):
    keys = request.session.keys()
    if 'id' not in keys:
        messages.success(request, "Session Expired! Please Login Again")
        return redirect('http://127.0.0.1:8000/home/login')


    if request.method == 'POST':
        dateval = request.POST['newelectDt']
        election.objects.filter(elect_status=0, elect_date__gt=datetime.date.today()).update(elect_date=dateval)
        messages.success(request, "Election postponed to "+dateval)
        return redirect('http://127.0.0.1:8000/home/admin')


    e=election.objects.filter(elect_status=0)
    if e.count()==0:
        messages.success(request, "No election to postpone")
        return redirect('http://127.0.0.1:8000/home/admin')

    if(e[0].elect_date<=datetime.date.today()):
        messages.success(request, "can't postpone now")
        return redirect('http://127.0.0.1:8000/home/admin')


    min=str(e[0].elect_date+datetime.timedelta(days=1))
    return render(request,'administrator/postpone.html',{'elecdate':e[0].elect_date,'min':min})

