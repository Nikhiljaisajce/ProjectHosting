"""College_Election URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('paneladd/',views.paneladd,name='paneladd'),
    path('deptadd/',views.deptadd,name='deptadd'),
    path('electionadd/',views.electionadd,name='electionadd'),
    path('staffadd/', views.staffadd, name='staffadd'),
    path('nomapprove/', views.nomapprove, name='nomapprove'),
    path('nompaper/',views.nompaper,name='nompaper'),
    path('symbol/',views.symboladd,name='symbol'),
    path('partyapprove/',views.partyapprove,name='deptapprove'),
    path('paneledit/',views.paneledit,name='paneledit'),
    path('deptadd/validate_dept/',views.validate_dept, name='validate_dept'),
    path('staffadd/validate_staff/',views.validate_staff, name='validate_staff'),
    path('nomwithdraw/',views.withdrawapprove,name='withdrawapprove'),
    path('resultPublish/',views.voteResult,name='resultPublish'),
    path('publish/',views.publishRes,name='publishResult'),
    path('deptrpt/',views.deptReport,name='deptRpt'),
    path('partyrpt/',views.partyReport,name='partyRpt'),
    path('staffrpt/',views.staffReport,name='staffRpt'),
    path('staffMgmt/',views.staffModify,name='staffMgmt'),
    path('postpone/',views.postpone,name='postpone'),


]
