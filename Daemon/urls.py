from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:_subj>/<slug:_type>/<slug:_title>/', views.gPageArg3 , name='gPageArg3'),
    path('all_pages/', views.all_pages, name='all_pages'),
    path('cPageF/', views.cPageF, name='cPageF'),
    path('cPageF/ufile/', views.upload_files, name='upldFile'),
    path('mPageF/<slug:_subj>/<slug:_type>/<slug:_title>/', views.mPageF, name='mPageF'),
    path('mdfy_new_page/', views.mdfy_new_page, name='mdfy_new_page'),
    path('upld_new_page/', views.upld_new_page, name='upld_new_page'),
    path('save_new_page/', views.save_new_page, name='save_new_page'),
    path('delete_page/<slug:_subj>/<slug:_type>/<slug:_title>/', views.delete_page, name='delete_page'),
    
]
