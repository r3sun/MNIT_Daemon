import os
import sys
sys.path.append("..")
from constants import Page_Storage

def creat_page_files(_subj, _type, _title, _cntnt):
    _url = Page_Storage + _subj + "/" + _type + "/" + _title
    _path = _url + "/index.html"
    if not os.path.exists(_url):
        os.makedirs(_url)
    os.path.join(_url, "index.html")
    p = open(_path, "w")
    p.write(_cntnt)
    p.close()
    return 1

def creat_upload_files(_subj, _type, _title, _f):
    _url = Page_Storage + _subj + "/" + _type + "/" + _title
    _path = _url + "/" + _f.name
    with open(_path, "wb+") as dfile:
        for c in _f.chunks():
            dfile.write(c)
    return 1;
