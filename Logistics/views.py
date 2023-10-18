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
from .models import DHL,CommercialInvoice,DoDnNumber,WesNewSg,CommercialPacl,InvoiceNumber,DoNumber,Proforma
from .forms import DHLForm,commercialinvoiceForm,dodnnumberForm,wesnewsgForm,commercialpaclForm,invoicenumberForm,donumberForm,proformaForm
from django.db.models import F,ExpressionWrapper, IntegerField



def logindex(request):

    return render(request, 'logindex.html')

def dhl(request):
    filter_FromCountry = request.GET.get('filter_FromCountry')
    filter_ToCountry = request.GET.get('filter_ToCountry')
    filter_Weight_Kg = request.GET.get('filter_Weight_Kg')

    test1 = DHL.objects.all()

    if filter_FromCountry:
        test1 = test1.filter(From_Country=filter_FromCountry)
    if filter_ToCountry:
        test1 = test1.filter(To_Country=filter_ToCountry)
    if filter_Weight_Kg:
        test1 = test1.filter(Weight_Kg=filter_Weight_Kg)

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
        'filter_FromCountry': filter_FromCountry,
        'filter_ToCountry': filter_ToCountry,
        'filter_Weight_Kg': filter_Weight_Kg,
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    
    return render(request, 'DHL/dhl.html', context)


def get_dropdown_options1(request):
 
    selected_fromcountry = request.GET.get('From_Country')
    test1 = DHL.objects.all()
    if selected_fromcountry:
        invoices = test1.filter(From_Country=selected_fromcountry)
        to_country_options = list(invoices.values_list('To_Country', flat=True).distinct())
        weight1_options = list(invoices.values_list('Weight_Kg', flat=True).distinct())
    else:
        to_country_options = []
        weight1_options = []
    
    response_data = {
        'to_country_options': to_country_options,
        'weight1_options': weight1_options,
    }
  
    return JsonResponse(response_data)


def get_dropdown_optionstocountry(request):

    selected_fromcountry = request.GET.get('From_Country') 
    selected_tocountry = request.GET.get('To_Country')
    test1 = DHL.objects.all()
    if selected_tocountry:
        invoices = test1.filter(From_Country=selected_fromcountry,To_Country=selected_tocountry)
        weight1_options = list(invoices.values_list('Weight_Kg', flat=True).distinct())
    else:

        weight1_options = []
    
    response_data = {
        'weight1_options': weight1_options,
    }
  
    return JsonResponse(response_data)


def dhlindex(request):
    if request.method == "POST":
        form = DHLForm(request.POST)
        if form.is_valid():
            form.save()
            filter_FromCountry  = form.cleaned_data['From_Country']
            filter_ToCountry  = form.cleaned_data['To_Country']
            filter_Weight_Kg = form.cleaned_data['Weight_Kg']
            url = reverse('Logistics:filter')
            url += f'?filter_FromCountry={filter_FromCountry}&filter_ToCountry={filter_ToCountry}&filter_Weight_Kg={filter_Weight_Kg}'
            return HttpResponseRedirect(url)
    else:
        form = DHLForm()


    if request.GET.get('filter_FromCountry'):
        filter_FromCountry1 = request.GET.get('filter_FromCountry')
        # Perform any filtering or processing based on the filter_ClientName value
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            selectedFromCountry = request.GET.get('selectedFromCountry')
            print(f"Received selected_client_name: { selectedFromCountry }")
            # Return a JSON response if it's an AJAX request
            return JsonResponse({'message': 'Filtered data'})
    test1 = DHL.objects.all()
  
    
    filter_FromCountry = request.GET.get('filter_FromCountry')
    filter_ToCountry = request.GET.get('filter_ToCountry')
    filter_Weight_Kg = request.GET.get('filter_Weight_Kg')

    print(filter_FromCountry)
    
    if filter_FromCountry:
        test1 = test1.filter(From_Country=filter_FromCountry)
    if filter_ToCountry:
        test1 = test1.filter(To_Country=filter_ToCountry)
    if filter_Weight_Kg:
        test1 = test1.filter(Weight_Kg=filter_Weight_Kg)

    unique_FromCountry = DHL.objects.order_by('From_Country').values_list('From_Country', flat=True).distinct()
    unique_ToCountry = DHL.objects.order_by('To_Country').values_list('To_Country', flat=True).distinct()
    unique_Weight_Kg = DHL.objects.order_by('Weight_Kg').values_list('Weight_Kg', flat=True).distinct()
        
    print('hi')
    context = {
        'form': form,
        'test1': test1,
        'filter_FromCountry': filter_FromCountry,
        'filter_ToCountry': filter_ToCountry,
        'filter_Weight_Kg': filter_Weight_Kg,
        'unique_FromCountry': unique_FromCountry,
        'unique_ToCountry': unique_ToCountry,  
        'unique_Weight_Kg': unique_Weight_Kg,   
    }
    return render(request, 'DHL/dhlindex.html', context)


def dhlexcel(request):
    filter_FromCountry = request.GET.get('filter_FromCountry')
    filter_ToCountry = request.GET.get('filter_ToCountry')
    filter_Weight1 = request.GET.get('filter_Weight1')

    filters = {}
    if filter_FromCountry:
        filters['From_Country'] = filter_FromCountry
    if filter_ToCountry:
        filters['To_Country'] = filter_ToCountry
    if filter_Weight1:
        filters['Weight_Kg'] = filter_Weight1

    test1 = DHL.objects.filter(**filters)

    # Define the desired fields for the CSV file
    fields = ['id'	,'WES_Ref',	'PO_NO'	,'Client_Name'	,'Ship_name',	'Client_Invoice_No'	,'INVOICE_DATE',	'Client_Frieght_Cost'	,'Client_Freight_Currency'
              	,'Client_Freight_Cost_in_SGD'	,'DHL_Invoice_number'	,'AWB_NUMBER'	,'AMOUNT_INR'	,'DHL_AMOUNT_SGD',	'DHL_DUTY_TAX'	,'Invoice_date2',	
                'Due_Date'	,'Status',	'Paid_date',	'Transaction_number'	,'From_Country'	, 'To_Country',	'Weight_Kg','Dimension_Volume', 'Dimension_CM' ,
                'Profit_and_Loss'	,'Remarks']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DHL.csv"'

    writer = csv.writer(response)
    
    try:
        # Write the header row
        writer.writerow(fields)

        # Write the data rows
        for data in test1:
            row = [getattr(data, field) for field in fields]
            writer.writerow(row)

    except Exception as e:
        print("Error:", e)

    return response

def adddhl(request):
    if request.method == "POST":
        form = DHLForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('Logistics:dhlindex')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = DHLForm()

    Client_Name = DHL.objects.exclude(Client_Name__exact='').order_by('Client_Name').values_list('Client_Name', flat=True).distinct()
    Ship_name = DHL.objects.exclude(Ship_name__exact='').order_by('Ship_name').values_list('Ship_name', flat=True).distinct()
    Status  = DHL.objects.exclude(Status__exact='').order_by('Status').values_list('Status', flat=True).distinct()
    From_Country  = DHL.objects.exclude(From_Country__exact='').order_by('From_Country').values_list('From_Country', flat=True).distinct()
    To_Country  = DHL.objects.exclude(To_Country__exact='').order_by('To_Country').values_list('To_Country', flat=True).distinct()
    Client_Freight_Currency = DHL.objects.exclude(Client_Freight_Currency__exact='').order_by('Client_Freight_Currency').values_list('Client_Freight_Currency', flat=True).distinct()
    last_id = DHL.objects.last().id if DHL.objects.exists() else 0
    context = {'last_id': last_id + 1} 
      

    context = {
        'ClientName_options': Client_Name,
        'shipname_options': Ship_name,
        'newstatus_options': Status,
        'From_Country_options': From_Country,
        'To_Country_options': To_Country,
        'form': form,
        'Client_Freight_Currency_options' : Client_Freight_Currency,
        'last_id': last_id + 1

    }
    return render(request, 'DHL/adddhl.html', context)
    
def addnewdhl(request):
    if request.method == "POST":
        form = DHLForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('Logistics:dhlindex')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = DHLForm()

    Client_Name = DHL.objects.exclude(Client_Name__exact='').order_by('Client_Name').values_list('Client_Name', flat=True).distinct()
    Ship_name = DHL.objects.exclude(Ship_name__exact='').order_by('Ship_name').values_list('Ship_name', flat=True).distinct()
    Status  = DHL.objects.exclude(Status__exact='').order_by('Status').values_list('Status', flat=True).distinct()
    From_Country  = DHL.objects.exclude(From_Country__exact='').order_by('From_Country').values_list('From_Country', flat=True).distinct()
    To_Country  = DHL.objects.exclude(To_Country__exact='').order_by('To_Country').values_list('To_Country', flat=True).distinct()
    Client_Freight_Currency = DHL.objects.exclude(Client_Freight_Currency__exact='').order_by('Client_Freight_Currency').values_list('Client_Freight_Currency', flat=True).distinct()
    last_id = DHL.objects.last().id if DHL.objects.exists() else 0
    context = {'last_id': last_id + 1} 
      

    context = {
        'ClientName_options': Client_Name,
        'shipname_options': Ship_name,
        'newstatus_options': Status,
        'From_Country_options': From_Country,
        'To_Country_options': To_Country,
        'form': form,
        'Client_Freight_Currency_options' : Client_Freight_Currency,
        'last_id': last_id + 1

    }
    return render(request, 'DHL/addnewdhl.html',context)


def updatedhl(request, data_id):
    data = get_object_or_404(DHL, pk=data_id)
    if request.method == 'POST': 
        form = DHLForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('Logistics:dhlindex')
    else:
        form = DHLForm(instance=data)
        
    shipname_data = DHL.objects.exclude(Ship_name__exact='').order_by('Ship_name').values_list('Ship_name', flat=True).distinct()
    Client_Name = DHL.objects.exclude(Client_Name__exact='').order_by('Client_Name').values_list('Client_Name', flat=True).distinct()
    To_Country = DHL.objects.exclude(To_Country__exact='').order_by('To_Country').values_list('To_Country', flat=True).distinct()
    From_Country = DHL.objects.exclude(From_Country__exact='').order_by('From_Country').values_list('From_Country', flat=True).distinct()
   
    
    context = {
        'form': form,
        'data_id': data_id,
        'shipname_options': shipname_data,
        'ClientName_options' : Client_Name,
        'From_Country':From_Country,
        'To_Country' : To_Country
        
    }
    return render(request, 'DHL/updatedhl.html', context)

def commercialinvoice(request):
    
    return render(request, 'WES-S-Numberseries/commercialinvoice.html')

def addci(request):
    if request.method == "POST":
        form = commercialinvoiceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:commercialinvoice')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = commercialinvoiceForm()

    last_id = CommercialInvoice.objects.last().ID if CommercialInvoice.objects.exists() else 0
    VESSEL_NAME = CommercialInvoice.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()

    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    
    
    } 
      
    return render(request, 'WES-S-Numberseries/addci.html',context)

def addnewci(request):
    if request.method == "POST":
        form = commercialinvoiceForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:commercialinvoice')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = commercialinvoiceForm()

    last_id = CommercialInvoice.objects.last().ID if CommercialInvoice.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    } 
      
    return render(request, 'WES-S-Numberseries/addnewci.html',context)
   
def commercialinvoiceci(request):
      
    
    test1 = CommercialInvoice.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-S-Numberseries/commercialinvoiceci.html', context)            

def dodnnumber(request):
 
  
    
    return render(request, 'WES-S-Numberseries/dodnnumber.html')
def adddn(request):
      
    if request.method == "POST":
        form = dodnnumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:dodnnumber')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = dodnnumberForm()

    last_id = DoDnNumber.objects.last().ID if DoDnNumber.objects.exists() else 0
    VESSEL_NAME = DoDnNumber.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()


    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    
    } 
      
    return render(request, 'WES-S-Numberseries/adddn.html',context)

def addnewdn(request):
    if request.method == "POST":
        form = dodnnumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:dodnnumber')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = dodnnumberForm()

    last_id = DoDnNumber.objects.last().ID if DoDnNumber.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    
    
    } 
      
    return render(request, 'WES-S-Numberseries/addnewdn.html',context)
def dodnnumberdn(request):
      
    test1 = DoDnNumber.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-S-Numberseries/dodnnumberdn.html', context)      
 


def wesnewsg(request):
  
   
    
    
    return render(request, 'WES-S-Numberseries/wesnewsg.html')
def addwns(request):
      
    if request.method == "POST":
        form = wesnewsgForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:wesnewsg')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = wesnewsgForm()

    last_id = WesNewSg.objects.last().ID if WesNewSg.objects.exists() else 0
    VESSEL_NAME = WesNewSg.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()

    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    
    } 
      
    return render(request, 'WES-S-Numberseries/addwns.html',context)
def addnewwns(request):
      
    if request.method == "POST":
        form = wesnewsgForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:wesnewsg')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = wesnewsgForm()

    last_id = WesNewSg.objects.last().ID if WesNewSg.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    
    
    } 
      
    return render(request, 'WES-S-Numberseries/addnewwns.html',context)
def wesnewsgwns(request):
   
    test1 = WesNewSg.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-S-Numberseries/wesnewsgwns.html', context)


def updateci(request, data_id):
    data = get_object_or_404(CommercialInvoice, pk=data_id)  # Use CommercialInvoice model
    if request.method == 'POST':
        form = commercialinvoiceForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:commercialinvoiceci')
    else:
        form = commercialinvoiceForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
    }
    return render(request, 'WES-S-Numberseries/updateci.html', context)    

def updatedn(request, data_id):
    data = get_object_or_404(DoDnNumber, pk=data_id)
    if request.method == 'POST':
        form = dodnnumberForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:dodnnumberdn')
    else:
        form = dodnnumberForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
       
    }
    return render(request, 'WES-S-Numberseries/updatedn.html', context)



def updatewns(request, data_id):
    data = get_object_or_404(WesNewSg, pk=data_id)
    if request.method == 'POST':
        form = wesnewsgForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:wesnewsgwns')
    else:
        form = wesnewsgForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
       
    }
    return render(request, 'WES-S-Numberseries/updatewns.html', context)  

  

def wessindex(request):
   
    return render(request, 'WES-S-Numberseries/wessindex.html') 

def wesiindex(request):
   
    return render(request, 'WES-I-Numberseries/wesiindex.html') 

def commercialpacl(request):    
    
    return render(request, 'WES-I-Numberseries/commercialpacl.html')

def addcp(request):
    if request.method == "POST":
        form = commercialpaclForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:commercialpacl')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = commercialpaclForm()

    last_id = CommercialPacl.objects.last().ID if CommercialPacl.objects.exists() else 0
    VESSEL_NAME = CommercialPacl.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()

    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    
    
    } 
      
    return render(request, 'WES-I-Numberseries/addcp.html',context)

def addnewcp(request):
    if request.method == "POST":
        form = commercialpaclForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:commercialpacl')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = commercialpaclForm()

    last_id = CommercialPacl.objects.last().ID if CommercialPacl.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    } 
      
    return render(request, 'WES-I-Numberseries/addnewcp.html',context)
   
def commercialpaclcp(request):
      
    
    test1 = CommercialPacl.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-I-Numberseries/commercialpaclcp.html', context)       



def updatecp(request, data_id):
    data = get_object_or_404(CommercialPacl, pk=data_id)  # Use CommercialInvoice model
    if request.method == 'POST':
        form = commercialpaclForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:commercialpaclcp')
    else:
        form = commercialpaclForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
    }
    return render(request, 'WES-S-Numberseries/updatecp.html', context) 

def invoicenumber(request):
   
    
    return render(request, 'WES-I-Numberseries/invoicenumber.html')

def addin(request):
    if request.method == "POST":
        form = invoicenumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:invoicenumber')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = invoicenumberForm()

    last_id = InvoiceNumber.objects.last().ID if InvoiceNumber.objects.exists() else 0
    VESSEL_NAME = InvoiceNumber.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()

    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    
    
    } 
      
    return render(request, 'WES-I-Numberseries/addin.html',context)

def addnewin(request):
    if request.method == "POST":
        form = invoicenumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:invoicenumber')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = invoicenumberForm()

    last_id = InvoiceNumber.objects.last().ID if InvoiceNumber.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    } 
      
    return render(request, 'WES-I-Numberseries/addnewin.html',context)
   
def invoicenumberin(request):
      
    
    test1 = InvoiceNumber.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-I-Numberseries/invoicenumberin.html', context)       



def updatein(request, data_id):
    data = get_object_or_404(InvoiceNumber, pk=data_id)  # Use CommercialInvoice model
    if request.method == 'POST':
        form = invoicenumberForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:invoicenumberin')
    else:
        form = invoicenumberForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
    }
    return render(request, 'WES-S-Numberseries/updatein.html', context)         


def donumber(request):
 
    return render(request, 'WES-I-Numberseries/donumber.html')

def adddo(request):
    if request.method == "POST":
        form = donumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:donumber')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = donumberForm()

    last_id = DoNumber.objects.last().ID if DoNumber.objects.exists() else 0
    VESSEL_NAME = DoNumber.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()

    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    
    
    } 
      
    return render(request, 'WES-I-Numberseries/adddo.html',context)

def addnewdo(request):
    if request.method == "POST":
        form = donumberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:donumber')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = donumberForm()

    last_id = DoNumber.objects.last().ID if DoNumber.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    } 
      
    return render(request, 'WES-I-Numberseries/addnewdo.html',context)
   
def donumberdo(request):
      
    
    test1 = DoNumber.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-I-Numberseries/donumberdo.html', context)       


def updatedo(request, data_id):
    data = get_object_or_404(DoNumber, pk=data_id)  # Use CommercialInvoice model
    if request.method == 'POST':
        form = donumberForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:donumberdo')
    else:
        form = donumberForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
    }
    return render(request, 'WES-I-Numberseries/updatedo.html', context)         

def proforma(request):
    
    return render(request, 'WES-S-Numberseries/proforma.html')

def addp(request):
    if request.method == "POST":
        form = proformaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:proforma')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = proformaForm()

    last_id = Proforma.objects.last().ID if Proforma.objects.exists() else 0
    VESSEL_NAME = Proforma.objects.exclude(VESSEL_NAME__exact='').order_by('VESSEL_NAME').values_list('VESSEL_NAME', flat=True).distinct()

    context = {
        
        'last_id': last_id + 1,
        'form': form,
        'VESSEL_NAME_options' : VESSEL_NAME
    } 
      
    return render(request, 'WES-I-Numberseries/addp.html',context)

def addnewp(request):
    if request.method == "POST":
        form = proformaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('testcase:proforma')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = proformaForm()

    last_id = Proforma.objects.last().ID if Proforma.objects.exists() else 0

    context = {
        
        'last_id': last_id + 1,
        'form': form
    
    } 
      
    return render(request, 'WES-I-Numberseries/addnewp.html',context)
   
def proformap(request):
      
    
    test1 = Proforma.objects.all().order_by('-ID')
   

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
       
        'total_rows':int(total_rows),
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'WES-I-Numberseries/proformap.html', context)       


def updatep(request, data_id):
    data = get_object_or_404(Proforma, pk=data_id)  # Use CommercialInvoice model
    if request.method == 'POST':
        form = proformaForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('testcase:proformap')
    else:
        form = proformaForm(instance=data) 
    
    context = {
        'form': form,
        'data_id': data_id,
    }
    return render(request, 'WES-I-Numberseries/updatep.html', context)     

def download_ci_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = CommercialInvoice.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CommercialInvoice.csv"'

    # Define the fields for the CSV file
    fields = ['ID','COMMERCIAL_NUMBER','PACKING_LIST_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE', 'Remarks']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response      

def download_dodnnumber_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = DoDnNumber.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DoDnNumber.csv"'

    # Define the fields for the CSV file
    fields = ['ID','DO_DN_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE', 'REMARK']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response       

def download_wesnewsg_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = WesNewSg.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="WesNewSg.csv"'

    # Define the fields for the CSV file
    fields = ['ID','INVOICE_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE', 'INVOICE_TYPE', 'SIGNED_DN', 'REMARK']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response        

def download_commercial_Pacl_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = CommercialPacl.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CommercialPacl.csv"'

    # Define the fields for the CSV file
    fields = ['ID','COMMERCIAL_NUMBER', 'PACL_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response        

def download_Invoice_Number_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = InvoiceNumber.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="InvoiceNumber.csv"'

    # Define the fields for the CSV file
    fields = ['ID','INVOICE_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE', 'REMARK']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response     

def download_Do_Number_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = DoNumber.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="DoNumber.csv"'

    # Define the fields for the CSV file
    fields = ['ID','DO_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response     

def download_Proforma_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = Proforma.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Proforma.csv"'

    # Define the fields for the CSV file
    fields = ['ID','PROFORMA_INVOICE_NUMBER', 'DATE', 'VESSEL_NAME', 'WES_NUMBER', 'PO_NUMBER', 'INCHARGE', 'STATUS', 'REMARK']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response


