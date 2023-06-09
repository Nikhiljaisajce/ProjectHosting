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
    path('partyadd/',views.party_reg,name='party_reg'),
    path('login/',views.Login,name='Login'),
    path('resetPassword/',views.resetPass,name='Login'),
    path('confirmPassword/',views.confirmPass,name='Login'),
    path('result/',views.electResults,name='Result'),
    path('department/', include('department.urls')),
  #  path('party/', include('party.urls')),
    path('student/',include('student.urls')),
    path('admin/',include('administrator.urls')),
   # path('staff/', include('staff.urls')),
    path('pollingpercent/',views.percent,name='percent'),
    path('electionDetails/',views.electDetails,name='electDetails'),



]
