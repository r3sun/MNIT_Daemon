import sys
from django.http.response import HttpResponse
sys.path.append("..")
from django.shortcuts import render
from django.utils import timezone
from .models import *
from .cpage import *
from Users.authentication import authenticate
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html', )

def gPageArg3(request, _subj, _type, _title):
    _url = _subj + "/" + _type + "/" + _title
    _path = _subj + "/" + _type + "/" + _title + "/index.html"
    try:
        p = PageInf.objects.get(url = _url)
        context = {
            "post_file": _path,
            "keywords": p.mk_array,
            "description": p.title,
            "author": p.author
        }
        return render(request, 'theme.html', context)
    except:
        return render(request, 'theme.html', {'pcontent' : '-_-'})

'''
def gPageArg1(request, _title):
    _path = _title + "/index.html"
    p = Pages.objects.get(path__icontains = _path)
    if p.aprnc == '1':
        return render(request, _path,)
    else:
        return render(request, 'index.html', {'pcontent' : '-_-'})
'''

def all_pages(request):
    p = PageInf.objects.all()
    content = { 'pages' : p }
    return render(request, 'all_pages.html', content)


def subj_pages(request, subj):
    p = PageInf.objects.filter(subj = subj)
    content = {'pages' : p}
    return render(request, 'subj-pages.html', content)

def cPageF(request):
    if authenticate(request):
        return render(request, 'create_page_form.html',)
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})

#get the form to modify page
def mPageF(request, _subj, _type, _title):
    if authenticate(request):
        _url = _subj + "/" + _type + "/" + _title
        try:
            p = PageInf.objects.get(url = _url)
            f = open(Page_Storage + p.path, 'r')
            c = f.read()
            context = {'title' : p.title, 'subj' : p.subj, 'typ' : p.typ, 'content' : c, 'mk_array' : p.mk_array}
            return render(request, 'modify_page_form.html', context)
        except:
            return render(request, 'msg.html', {'msg' : 'page with this url doesn\'t exists'})
    else:
        return render(request, 'user/login.html', {'notification' : 'non-auhenticated user'})

#upload new page
def upld_new_page(request):
    if authenticate(request):
        if request.method == 'POST':
            _title = request.POST['_title']
            _utitle = _title.replace(" ", "_")
            _subj = request.POST['_subj']
            _type = request.POST['_type']
            _cntnt = request.POST['_cntnt']
            _mk_array = request.POST['_mk_array']
            _author = request.session['_user']
            _url = _subj + "/" + _type + "/" + _utitle
            _path = _url + "/index.html"
            try:
                p = Pages.objects.get(url = _url)
                return render(request, 'msg.html', {'msg' : 'page with the same name already exists'})
            except:
                c = creat_page_files(_url, _cntnt)
                try:
                    f = mv_static_file_to_orgn(_url)
                except:
                    f = 1
                if c and f:
                    p = Pages(url = _url)
                    pinf = PageInf(path = _path, url = _url, title = _title, subj = _subj, typ = _type, pub_time = timezone.now(), last_modified = timezone.now(), mk_array = _mk_array, author = _author)
                    pinf.save()
                    p.save()
                    return render(request, _path, )
                else:
                    return render(request, 'msg.html', {'msg' : 'couldn\'t creat page'})
        else:
            return render(request, 'msg.html', {'msg' : 'method isn\'t post'})
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})

def save_new_page(request):
    if authenticate(request):
        if request.method == 'POST':
            _title = request.POST['_title']
            _utitle = _title.replace(" ", "_")
            _subj = request.POST['_subj']
            _type = request.POST['_type']
            _cntnt = request.POST['_cntnt']
            _mk_array = request.POST['_mk_array']
            _author = request.session['_user']
            _url = _subj + "/" + _type + "/" + _utitle
            _path = _url + "/index.html"
            try:
                p = Pages.objects.get(url = _url)
                return render(request, 'msg.html', {'msg' : 'page with the same name already exists'})
            except:
                c = creat_page_files(_url, _cntnt)
                try:
                    f = mv_static_file_to_orgn(_url)
                except:
                    f = 1
                if c and f:
                    p = Pages(url = _url)
                    p.save()
                    pinf = PageInf(path = _path, url = _url, title = _title, subj = _subj, typ = _type, pub_time = timezone.now(), mk_array = _mk_array, author = _author)
                    pinf.save()
                    return render(request, _path, )
                else:
                    return render(request, 'msg.html', {'msg' : 'couldn\'t creat page'})
            else:
                return render(request, 'msg.html', {'msg' : 'page with the same name already exists'})
        else:
            return render(request, 'msg.html', {'msg' : 'method isn\'t post'})
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})

def delete_page(request, _subj, _type, _title):
    if authenticate(request):
        _url = _subj + "/" + _type + "/" + _title
        p = Pages.objects.get(url = _url)
        pinf = PageInf.objects.get(url = _url)
        try:
            dpf = del_page_file(_url)
        except:
            dpf = None
        if dpf:
            dp = Deltd_Pages(path = pinf.path, url = pinf.url, title = pinf.title, subj = pinf.subj, typ = pinf.typ, pub_time = pinf.pub_time, last_modified = pinf.last_modified, mk_array = pinf.mk_array, author = pinf.author)
            dp.save()
            pinf.delete()
            p.delete()
            response = HttpResponse("successfully deleted page")
            response.status_code = 200
            return response
        else:
            response = HttpResponse("could not deleted page")
            response.status_code = 204
            return response
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})


def mdfy_new_page(request):
    if authenticate(request):
        if request.method == 'POST':
            _ititle = request.POST['_ititle']
            _iutitle = _ititle.replace(" ", "_")
            _title = request.POST['_title']
            _utitle = _title.replace(" ", "_")
            _isubj = request.POST['_isubj']
            _subj = request.POST['_subj']
            _itype = request.POST['_itype']
            _type = request.POST['_type']
            _cntnt = request.POST['_cntnt']
            _imk_array = request.POST['_imk_array']
            _mk_array = request.POST['_mk_array']
            _author = request.session['_user']
            _iurl = _isubj + "/" + _itype + "/" + _iutitle
            _ipath = _iurl + "/index.html"
            _url = _subj + "/" + _type + "/" + _utitle
            _path = _url + "/index.html"
            try:
                p = Pages.objects.get(url = _iurl)
                pinf = PageInf.objects.get(url = _iurl)
                try:
                    cpy = cpy_page_file(_iurl, _url)
                except:
                    cpy = 0
                try:
                    crt = creat_page_files(_url, _cntnt)
                except:
                    crt = 0
                try:
                    mv = mv_static_file_to_orgn(_url)
                except:
                    mv = 0
                m = Mdfd_Pages(url = p.url, path = pinf.path, title = pinf.title, subj = pinf.subj, typ = pinf.typ, pub_time = pinf.pub_time, last_modified = pinf.last_modified, mk_array = pinf.mk_array, author = pinf.author)
                m.save()
                pinf.url = _url
                pinf.path = _path
                pinf.title = _title
                pinf.subj = _subj
                pinf.typ = _type
                pinf.last_modified = timezone.now()
                pinf.mk_array = _mk_array
                pinf.author = _author
                pinf.save()
                p.url = _url
                p.save()
                return render(request, 'msg.html', {'msg' : 'successfully modified page'})
            except:
                return render(request, 'msg.html', {'msg' : 'couldn\'t modify page'})
        else:
            return render(request, 'msg.html', {'msg' : 'method isn\'t post'})
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})


def upload_files(request):
    if authenticate(request):
        if request.method == 'POST':
            _title = request.POST['_title']
            _utitle = _title.replace(" ", "_")
            _subj = request.POST['_subj']
            _type = request.POST['_type']
            if request.FILES:
                d = []
                for f in request.FILES.getlist('_files'):
                    if "image" in f.content_type or "text" in f.content_type or "html" in f.content_type or "css" in f.content_type or "javascript" in f.content_type or "python" in f.content_type:
                        creat_upload_files(_subj, _type, _utitle, f)
                        file = {"name" : f.name, "url" : "/static/" + _subj + "/" + _type + "/" + _utitle + "/" + f.name, "type" : f.content_type}
                        d.append(file)
                    else:
                        file = {"warning" : "non-supported file", "name" : f.name}
                        d.append(file)
                return JsonResponse(d, safe=False)
            else:
                d = [{"name" : "null", "url" : "null"}]
                return JsonResponse(d, safe=False)
        else:
            return render(request, 'msg.html', {'msg' : 'method isn\'t post'})
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})


'''                
def viewed(request):
    v_url = request.Post['_url']
    v_region = request.Post['_region']
    v_time = request.Post['_time']
    p = Pagedb.objects.filter(url = v_url)
    p._view += 1
    p.pg_views_set.create(region = v_region, _time = v_time)
'''
