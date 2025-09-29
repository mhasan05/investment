from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def login(request):
    return render(request,'user_auth/login.html')


def dashboard(request):
    return render(request,'user_dashboard.html')