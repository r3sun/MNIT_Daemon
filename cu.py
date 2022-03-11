from Users.models import Credentials

def creat_user():
    n = input("name  :")
    p = input("password :")
    u = Credentials(name = n, password = p)
    u.save()
    print("done")
    
creat_user()
