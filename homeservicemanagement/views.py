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