from .models import Credentials
from .encrypt_password import encrypt

def authenticate(request):
    if '_user' in request.session:
        u = Credentials.objects.get(name__icontains = request.session['_user'])
        if u and u.password == encrypt(request.session['_password']):
            return 1
        else:
            return 0
    else:
        return 0

