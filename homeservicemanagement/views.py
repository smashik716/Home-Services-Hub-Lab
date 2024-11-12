from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
import datetime
from django.core.exceptions import ObjectDoesNotExist




# Create your views here.
def notification():
    status = Status.objects.get(status='pending')
    new = Service_Man.objects.filter(status=status)
    count = 0
    for i in new:
        count += 1
    d = {'count': count, 'new': new}
    return d


def Home(request):
    user = ""
    error = ""
    try:
        user = User.objects.get(id=request.user.id)
        try:
            sign = Customer.objects.get(user=user)
            error = "pat"
        except:
            pass
    except:
        pass
    ser1 = Service_Man.objects.all()
    ser = Service_Category.objects.all()
    for i in ser:
        count = 0
        for j in ser1:
            if i.category == j.service_name:
                count += 1
        i.total = count
        i.save()
    d = {'error': error, 'ser': ser}
    return render(request, 'home.html', d)


def contact(request):
    error = False
    if request.method == "POST":
        n = request.POST['name']
        e = request.POST['email']
        m = request.POST['message']
        status = Status.objects.get(status="unread")
        Contact.objects.create(status=status, name=n, email=e, message1=m)
        error = True
    d = {'error': error}
    return render(request, 'contact.html', d)





def about(request):
    return render(request, 'about.html')


def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Customer.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                stat = Status.objects.get(status="Accept")
                pure = False
                try:
                    pure = Service_Man.objects.get(status=stat, user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error = "notmember"

        else:
            error = "not"
    d = {'error': error}
    return render(request, 'login.html', d)





def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        con = request.POST['contact']
        add = request.POST['address']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f, last_name=l)
        if type == "customer":
            Customer.objects.create(user=user, contact=con, address=add, image=im)
        else:
            stat = Status.objects.get(status='pending')
            Service_Man.objects.create(doj=dat, image=im, user=user, contact=con, address=add, status=stat)
        error = "create"
    d = {'error': error}
    return render(request, 'signup.html', d)


def User_home(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        pass
    d = {'error': error}
    return render(request, 'user_home.html', d)


def Service_home(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terro = ""
    if None == sign.service_name:
        terro = "message"
    else:
        if sign.status.status == "pending":
            terro = "message1"
    d = {'error': error, 'terro': terro}
    return render(request, 'service_home.html', d)