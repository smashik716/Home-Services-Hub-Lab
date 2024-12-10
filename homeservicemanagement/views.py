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


def Admin_Home(request):
    dic = notification()
    cus = Customer.objects.all()
    ser = Service_Man.objects.all()
    cat = Service_Category.objects.all()
    count1 = 0
    count2 = 0
    count3 = 0
    for i in cus:
        count1 += 1
    for i in ser:
        count2 += 1
    for i in cat:
        count3 += 1
    d = {'new': dic['new'], 'count': dic['count'], 'customer': count1, 'service_man': count2, 'service': count3}
    return render(request, 'admin_home.html', d)


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


def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error = "pat"
        else:
            error = "not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)


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


def Service_Order(request):
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
    order = Order.objects.filter(service=sign)
    d = {'error': error, 'terro': terro, 'order': order}
    return render(request, 'service_order.html', d)


def Admin_Order(request):
    dic = notification()
    order = Order.objects.all()
    d = {'order': order, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'admin_order.html', d)


def Customer_Order(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.filter(customer=sign)
    d = {'error': error, 'order': order}
    return render(request, 'customer_order.html', d)


def Customer_Booking(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    terror = False
    ser1 = Service_Man.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        add = request.POST['add']
        dat = request.POST['date']
        da = request.POST['day']
        ho = request.POST['hour']
        st = Status.objects.get(status="pending")
        Order.objects.create(status=st, service=ser1, customer=sign, book_date=dat, book_days=da, book_hours=ho)
        terror = True
    d = {'error': error, 'ser': sign, 'terror': terror}
    return render(request, 'booking.html', d)


def Booking_detail(request, pid):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
        pass
    order = Order.objects.get(id=pid)
    d = {'error': error, 'order': order}
    return render(request, 'booking_detail.html', d)


def All_Service(request):
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
    return render(request, 'services.html', d)


def Explore_Service(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
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
    ser = Service_Category.objects.get(id=pid)
    sta = Status.objects.get(status="Accept")
    order = Service_Man.objects.filter(service_name=ser.category, status=sta)
    d = {'error': error, 'ser': ser, 'order': order}
    return render(request, 'explore_services.html', d)


def Logout(request):
    logout(request)
    return redirect('home')


def Edit_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image = i
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        sign.address = ad
        sign.contact = con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.save()
        terror = True
    d = {'terror': terror, 'error': error, 'pro': sign, 'ser': ser}
    return render(request, 'edit_profile.html', d)

def Edit_Service_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    car = ID_Card.objects.all()
    city = City.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image = i
            sign.save()
        except:
            pass
        try:
            i1 = request.FILES['image1']
            sign.id_card = i1
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        se = request.POST['service']
        card = request.POST['card']
        cit = request.POST['city']
        ex = request.POST['exp']
        dob = request.POST['dob']
        if dob:
            sign.dob = dob
            sign.save()
        ci = City.objects.get(city=cit)
        sign.address = ad
        sign.contact = con
        sign.city = ci
        user.first_name = f
        user.last_name = l
        user.email = e
        sign.id_type = card
        sign.experience = ex
        sign.service_name = se
        user.save()
        sign.save()
        terror = True
    d = {'city': city, 'terror': terror, 'error': error, 'pro': sign, 'car': car, 'ser': ser}
    return render(request, 'edit_service_profile.html', d)


def Edit_Admin_Profile(request):
    dic = notification()
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Customer.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image = i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact = con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        pro.save()
        error = True
    d = {'error': error, 'pro': pro, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'edit_admin_profile.html', d)


def profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro': sign, 'error': error}
    return render(request, 'profile.html', d)


def service_profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro': sign, 'error': error}
    return render(request, 'service_profile.html', d)
def Edit_Service_Profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    car = ID_Card.objects.all()
    city = City.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image = i
            sign.save()
        except:
            pass
        try:
            i1 = request.FILES['image1']
            sign.id_card = i1
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        se = request.POST['service']
        card = request.POST['card']
        cit = request.POST['city']
        ex = request.POST['exp']
        dob = request.POST['dob']
        if dob:
            sign.dob = dob
            sign.save()
        ci = City.objects.get(city=cit)
        sign.address = ad
        sign.contact = con
        sign.city = ci
        user.first_name = f
        user.last_name = l
        user.email = e
        sign.id_type = card
        sign.experience = ex
        sign.service_name = se
        user.save()
        sign.save()
        terror = True
    d = {'city': city, 'terror': terror, 'error': error, 'pro': sign, 'car': car, 'ser': ser}
    return render(request, 'edit_service_profile.html', d)


def Edit_Admin_Profile(request):
    dic = notification()
    error = False
    user = User.objects.get(id=request.user.id)
    pro = Customer.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            pro.image = i
            pro.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        pro.address = ad
        pro.contact = con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        pro.save()
        error = True
    d = {'error': error, 'pro': pro, 'new': dic['new'], 'count': dic['count']}
    return render(request, 'edit_admin_profile.html', d)


def profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro': sign, 'error': error}
    return render(request, 'profile.html', d)


def service_profile(request):
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Customer.objects.get(user=user)
        error = "pat"
    except:
        sign = Service_Man.objects.get(user=user)
    terror = False
    d = {'pro': sign, 'error': error}
    return render(request, 'service_profile.html', d)

def admin_profile(request):
    try:
        customer = Customer.objects.get(user=request.user)  # Assuming you're using a user field in Customer model
        # Your view logic for existing customer
        return render(request, 'admin_profile.html', {'customer': customer})
    except ObjectDoesNotExist:
        # Handle the case where the customer does not exist
        return redirect('some_other_url')
