import sys
sys.path.append("..")
from django.shortcuts import render
from .models import Credentials
from .encrypt_password import encrypt
from .authentication import authenticate
from Daemon.models import Pages, PageInf
from django.core import serializers
from django.http import JsonResponse

# Create your views here.

def login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            u = Credentials.objects.get(name = request.POST['_user'])
            if u and u.password == request.POST['_pswrd']:
                request.session['_user'] = u.name
                request.session['_password'] = encrypt(u.password)
                request.session.delete_test_cookie()
                request.session.set_test_cookie()
                return render(request, 'user/home.html', )
            else:
                request.session.set_test_cookie()
                return render(request, 'user/login.html', {'notification' : 'wrong credentials'})
        else:
            request.session.set_test_cookie()
            return render(request, 'user/msg.html', {'msg' : 'enable cookie and try again'})
    else:
        request.session.set_test_cookie()
        return render(request, 'user/login.html', {'notification' : 'method is not "POST"'})

def logout(request):
    request.session.flush()
    return render(request, 'user/login.html', )

def getLoginF(request):
    request.session.set_test_cookie()
    return render(request, 'user/login.html', )

def get_cPageF(request):
    context = {'url' : '/cPageF/'}
    request.session.delete_test_cookie()
    request.session.set_test_cookie()
    return render(request, 'user/pass.html', context)

def auther_pages(request):
    if authenticate(request):
        context = {'title' : 'My Pages', 'main_url' : 'http://127.0.0.1:8000'}
        request.session.delete_test_cookie()
        request.session.set_test_cookie()
        return render(request, 'user/author_pages.html', context)
    else:
        request.session.set_test_cookie()
        return render(request, 'user/login.html', {'notification' : 'wrong credentials'})

def get_auther_pages(request, offset):
    if authenticate(request):
        p = PageInf.objects.filter(author__icontains = request.session['_user']).order_by("-pub_time")[offset:offset + 8]
        if p.count() > 0:
            print(p.count())
            d = serializers.serialize('json', p)
            request.session.delete_test_cookie()
            request.session.set_test_cookie()
            return JsonResponse(d, safe=False)
        else:
            request.session.delete_test_cookie()
            request.session.set_test_cookie()
            return JsonResponse(None, safe=False)
    else:
        request.session.set_test_cookie()
        return render(request, 'user/login.html', {'notification' : 'wrong credentials'})

def settings(request):
    if authenticate(request):
        request.session.delete_test_cookie()
        request.session.set_test_cookie()
        context = {'title' : 'My Pages', 'main_url' : 'http://127.0.0.1:8000'}
        return render(request, 'user/settings.html', context)
    else:
        request.session.set_test_cookie()
        return render(request, 'user/login.html', {'notification' : 'wrong credentials'})


def home(request):
    if authenticate(request):
        request.session.delete_test_cookie()
        request.session.set_test_cookie()
        context = {'title' : 'My Pages', 'main_url' : 'http://127.0.0.1:8000'}
        return render(request, 'user/home.html', )
    else:
        request.session.set_test_cookie()
        return render(request, 'user/login.html', {'notification' : 'wrong credentials'})


def chg_name(request):
    if authenticate(request):
        if request.method == 'POST':
            u = Credentials.objects.get(name = request.session['_user'])
            if u and request.POST['password'] == u.password:
                u.name = request.POST['uname']
                u.save()
                context = {'title' : 'My Pages', 'main_url' : 'http://127.0.0.1:8000', 'notification' : 'Name has been changed'}
                request.session['_user'] = u.name
                return render(request, 'user/settings.html', context)
            else:
                return render(request, 'user/settings.html', {'notification' : 'wrong Password'})
        else:
            return render(request, 'user/login.html', {'notification' : 'method is not "POST"'})
    else:
        return render(request, 'user/login.html', {'notification' : 'wrong credentials'})

def chg_password(request):
    if authenticate(request):
        if request.method == 'POST':
            u = Credentials.objects.get(name = request.session['_user'])
            if u and request.POST['password'] == u.password:
                nw = request.POST['nw_password']
                c_nw = request.POST['c_nw_password']
                if nw == c_nw:
                    u.password = request.POST['nw_password']
                    u.save()
                    context = {'title' : 'My Pages', 'main_url' : 'http://127.0.0.1:8000', 'notification' : 'Password has been changed'}
                    return render(request, 'user/settings.html', context)
                else:
                    context = {'title' : 'My Pages', 'main_url' : 'http://127.0.0.1:8000', 'notification' : 'new password and confirm password didn\'t match'}
                    return render(request, 'user/settings.html', context)
            else:
                return render(request, 'user/settings.html', {'notification' : 'wrong Password'})
        else:
            return render(request, 'user/login.html', {'notification' : 'method is not "POST"'})
    else:
        return render(request, 'user/login.html', {'notification' : 'wrong credentials'})

