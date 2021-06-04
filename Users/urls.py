from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('loginForm/', views.getLoginF, name='loginForm'),
    #path('user/', views.user, name='user'),
    path('pages/', views.auther_pages, name='pages'),
    path('get_pages/<int:offset>', views.get_auther_pages, name='get_pages'),
    #path('chat/', views.chat, name='chat'),
    #path('notification/', views.notification, name='notification'),
    path('settings/', views.settings, name='settings'),
    path('chg_name/', views.chg_name, name='chg_name'),
    path('chg_password/', views.chg_password, name='chg_password'),
    path('get_cPageF/', views.get_cPageF, name='get_CPageF'),
]
