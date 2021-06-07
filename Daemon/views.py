import sys
sys.path.append("..")
from django.shortcuts import render
from django.utils import timezone
from .models import Pages
from .cpage import *
from Users.authentication import authenticate
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html', )

def gPageArg3(request, _subj, _type, _title):
    _path = _subj + "/" + _type + "/" + _title + "/index.html"
    p = Pages.objects.get(path__icontains = _path)
    if p.state == '1' and p.aprnc == '1':
        return render(request, _path,)
    else:
        return render(request, 'index.html', {'pcontent' : '-_-'})

def gPageArg1(request, _title):
    _path = _title + "/index.html"
    p = Pages.objects.get(path__icontains = _path)
    if p.aprnc == '1':
        return render(request, _path,)
    else:
        return render(request, 'index.html', {'pcontent' : '-_-'})


def all_pages(request):
    p = Pages.objects.filter(aprnc = '1')
    content = { 'pages' : p }
    return render(request, 'all_pages.html', content)


def subj_pages(request, subj):
    p = Pages.objects.filter(subj = subj).filter(state = '1').filter(aprnc = '1')
    content = {'pages' : p}
    return render(request, 'subj-pages.html', content)

def cPageF(request):
    if authenticate(request):
        return render(request, 'create_page_form.html',)
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})

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
                c = creat_page_files(_subj, _type, _utitle, _cntnt)
                f = mv_file_to_orgn(_subj, _type, _utitle)
                if c and f:
                    p = Pages(path = _path, url = _url, title = _title, subj = _subj, typ = _type, pub_time = timezone.now(), mk_array = _mk_array, author = _author, aprnc = '1', state = '1')
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
                c = creat_page_files(_subj, _type, _utitle, _cntnt)
                f = mv_file_to_orgn(_subj, _type, _utitle)
                if c and f:
                    p = Pages(path = _path, url = _url, title = _title, subj = _subj, typ = _type, pub_time = timezone.now(), mk_array = _mk_array, author = _author, aprnc = '0', state='1')
                    p.save()
                    return render(request, _path, )
                else:
                    return render(request, 'msg.html', {'msg' : 'couldn\'t creat page'})
            else:
                return render(request, 'msg.html', {'msg' : 'page with the same name already exists'})
        else:
            return render(request, 'msg.html', {'msg' : 'method isn\'t post'})
    else:
        return render(request, 'login.html', {'notification' : 'non-auhenticated user'})

def delete_page(request):
    if authenticate(request):
        if request.method == 'POST':
            p = Pages.objects.get(url = request.POST['_url'])
            p.state = '0'
            p.save()
            return render(request, 'msg.html', {'msg' : 'deleted successfuly'})
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

                
#def viewed(request):
#    v_url = request.Post['_url']
#    v_region = request.Post['_region']
#    v_time = request.Post['_time']
#    p = Pagedb.objects.filter(url = v_url)
#    p._view += 1
#    p.pg_views_set.create(region = v_region, _time = v_time)
    
