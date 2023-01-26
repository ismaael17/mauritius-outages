from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def index(request):
    return render(request, 'outages/index.html')

def search_results(request):
    if request.method == 'GET':
        location = request.GET.get('location')
        outages = Outage.objects.filter(location__contains=location)
        return render(request, 'outages/search_results.html', {'outages': outages})


    
