from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from io import BytesIO 
from xhtml2pdf import pisa  
from django.http import HttpResponse
import csv
from django.http import JsonResponse
import os
from django.db.models import Q
from django.conf import settings
from decimal import Decimal
from django.db import transaction
from django_pivot.pivot import pivot
from collections import defaultdict
from PIL import Image
import base64
from django.contrib import messages
from index.models import Login,Logisticslogin
# from .forms import SOAForm,DHLForm,commercialinvoiceForm,packinglistForm,dodnnumberForm,wesnewsgForm
from django.db.models import F,ExpressionWrapper, IntegerField



def loginindex(request):

    return render(request, 'loginindex.html')


def Accountslogin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Try to retrieve the user from the database
            user = Login.objects.get(username=username)
            
            
            if user.password == password:
                # Passwords match, consider the user as logged in
                request.session['user_id'] = user.id
                return redirect('Accounts:index') 
               
               
            else:
                
                messages.error(request, 'Invalid username or password!')
        except Login.DoesNotExist:
            messages.error(request, 'User does not exist!')
    return render(request, 'accountslogin.html')        

def Logistics(request):
    

    print('hidishdsudsjdhsdsjdsjdsjdsjdshn')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Try to retrieve the user from the database
            user = Logisticslogin.objects.get(username=username)
            print(user)
            
            if user.password == password:
                # Passwords match, consider the user as logged in
                request.session['user_id'] = user.id
                return redirect('Logistics:logindex') 
                
               
            else:
                
                messages.error(request, 'Invalid username or password!')
        except Logisticslogin.DoesNotExist:
            messages.error(request, 'User does not exist!')
    return render(request, 'Logistics.html')


def Procurement(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Try to retrieve the user from the database
            user = Login.objects.get(username=username)
            
            
            if user.password == password:
                # Passwords match, consider the user as logged in
                request.session['user_id'] = user.id
                return redirect('Accounts:index') 
                
               
            else:
                
                messages.error(request, 'Invalid username or password!')
        except Login.DoesNotExist:
            messages.error(request, 'User does not exist!')            

    return render(request, 'accountslogin.html')

def Management(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Try to retrieve the user from the database
            user = Login.objects.get(username=username)
            
            
            if user.password == password:
                # Passwords match, consider the user as logged in
                request.session['user_id'] = user.id
                return redirect('Accounts:index') 
                
               
            else:
                
                messages.error(request, 'Invalid username or password!')
        except Login.DoesNotExist:
            messages.error(request, 'User does not exist!')

def Viewonly(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            # Try to retrieve the user from the database
            user = Login.objects.get(username=username)
            
            
            if user.password == password:
                # Passwords match, consider the user as logged in
                request.session['user_id'] = user.id
                return redirect('Accounts:index') 
                
               
            else:
                
                messages.error(request, 'Invalid username or password!')
        except Login.DoesNotExist:
            messages.error(request, 'User does not exist!')

