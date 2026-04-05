from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime

@login_required(login_url='/login/')
def home(request):
    return render(request, 'html/home1.html')


def guide(request):
    return render(request, 'html/guide.html')