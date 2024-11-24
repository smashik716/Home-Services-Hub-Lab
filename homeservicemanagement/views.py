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
