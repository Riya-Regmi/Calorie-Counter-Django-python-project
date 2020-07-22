from django.contrib import admin
from django.urls import path
from . import views
from django.urls import re_path


urlpatterns=[   
    path('',views.home ,name="home"),
    path('login/',views.user_login,name='login'),
    path('signup/',views.signup,name='signup'),
    path(r'^profile/(?P<username>\w+)$',views.profile,name='profile'),
    path(r'^calculate/(?P<username>\w+)$',views.calculate,name='calculate'),
    path(r'^historyday/(?P<username>\w+)$',views.historyday,name='historyday'),
    path(r'^historyweek/(?P<username>\w+)$',views.historyweek,name='historyweek'),
    path(r'^historymonth/(?P<username>\w+)$',views.historymonth,name='historymonth'),


]    