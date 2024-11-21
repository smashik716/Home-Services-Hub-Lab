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
