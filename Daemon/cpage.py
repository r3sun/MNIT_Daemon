import os
import sys
sys.path.append("..")
from constants import *
import shutil
import datetime

def creat_page_files(_subj, _type, _title, _cntnt):
    _path = Page_Storage + _subj + "/" + _type + "/" + _title
    _file = _path + "/index.html"
    if not os.path.exists(_path):
        os.makedirs(_path)
    os.path.join(_path, "index.html")
    p = open(_file, "w")
    p.write(_cntnt)
    p.close()
    return 1

def creat_upload_files(_subj, _type, _title, _f):
    _path = Static_Files_Storage + _subj + "/" + _type + "/" + _title
    _file = _path + "/" + _f.name
    if not os.path.exists(_path):
        os.makedirs(_path)
    with open(_file, "wb+") as dfile:
        for c in _f.chunks():
            dfile.write(c)
    return 1;

def mv_file_to_orgn(_url):
    _fpath = Static_Files_Storage + _url
    _tpath = Page_Storage + _url
    cpy = shutil.copytree(_fpath, _tpath, dirs_exist_ok=True)
    if cpy:
        shutil.rmtree(_fpath)
        return 1
    else:
        return 0

def del_page_file(_url):
    _fpath = Page_Storage + _url
    _tpath = Deleted_Page_Storage + _url
    cpy = shutil.copytree(_fpath, _tpath, dirs_exist_ok=True)
    if cpy:
        shutil.rmtree(_fpath)
        return 1
    else:
        return 0

def mdfy_page_file(_url):
    dt = datetime.datetime.now()
    dt = str(dt)
    dt = dt.replace(" ", "_").replace("-", "_").replace(":", "_").replace(".", "_")
    _fpath = Page_Storage + _url
    _tpath = Modified_Page_Storage + _url + "/" + dt
    cpy = shutil.copytree(_fpath, _tpath, dirs_exist_ok=True)
    if cpy:
        shutil.rmtree(_fpath)
        return 1
    else:
        return 0
