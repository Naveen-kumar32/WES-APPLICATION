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
from .models import SOA
from .forms import SOAForm
from django.db.models import F,ExpressionWrapper, IntegerField








def get_dropdown_options(request):

    selected_client = request.GET.get('ClientName')
    print(selected_client)
    test1 = SOA.objects.all()
    if selected_client:
        invoices = test1.filter(ClientName=selected_client)
        new_status_options = list(invoices.values_list('newstatus', flat=True).distinct())
        currency_options = list(invoices.values_list('currency1', flat=True).distinct())

        new_status_options.sort(reverse=True)
    else:
        new_status_options = []
        currency_options = []

    newstatus= []
    for i in new_status_options:
        if i == 'NOT_PAID':
            newstatus.append("NOT_PAID")

        elif i == "PAID":
            newstatus.append("PAID")
        elif i == "ORDER_PROCESSING":
            newstatus.append("ORDER_PROCESSING")
    newstatus.sort()

    print(newstatus)
    response_data = {
        'new_status_options': newstatus,
        'currency_options': currency_options,
    }


    return JsonResponse(response_data)

def get_dropdown_optionsnewstatus(request):

    selected_client = request.GET.get('ClientName')
    selected_newstatus = request.GET.get('newstatus')
    test1 = SOA.objects.all()
    if selected_client:
        invoices = test1.filter(ClientName=selected_client,newstatus=selected_newstatus)
        currency_options = list(invoices.values_list('currency1', flat=True).distinct())
    else:
        currency_options = []

    response_data = {

        'currency_options': currency_options,
    }

    return JsonResponse(response_data)

def index(request):

   
    return render(request, 'index.html')


def soaindex(request):
    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()
            filter_ClientName = form.cleaned_data['ClientName']
            filter_newstatus = form.cleaned_data['newstatus']
            filter_currency1 = form.cleaned_data['currency1']
            url = reverse('Accounts:filter')
            url += f'?filter_ClientName={filter_ClientName}&filter_newstatus={filter_newstatus}&filter_currency1={filter_currency1}'
            return HttpResponseRedirect(url)
    else:
        form = SOAForm()


    if request.GET.get('filter_ClientName'):
        filter_ClientName1 = request.GET.get('filter_ClientName')
        # Perform any filtering or processing based on the filter_ClientName value

        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            # Return a JSON response if it's an AJAX request
            return JsonResponse({'message': 'Filtered data'})
    test1 = SOA.objects.all()


    filter_ClientName = request.GET.get('filter_ClientName')
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')

    if filter_ClientName:
        test1 = test1.filter(ClientName=filter_ClientName)
    if filter_newstatus:
        test1 = test1.filter(newstatus=filter_newstatus)
    if filter_currency1:
        test1 = test1.filter(currency1=filter_currency1)

    unique_clients = SOA.objects.order_by('ClientName').values_list('ClientName', flat=True).distinct()
    unique_newstatuses = SOA.objects.order_by('newstatus').values_list('newstatus', flat=True).distinct()
    unique_currencies = SOA.objects.order_by('currency1').values_list('currency1', flat=True).distinct()

   
    context = {
        'form': form,
        'test1': test1,
        'filter_ClientName': filter_ClientName,
        'filter_newstatus': filter_newstatus,
        'filter_currency1': filter_currency1,
        'unique_clients': unique_clients,
        'unique_newstatuses': unique_newstatuses,
        'unique_currencies': unique_currencies,
    }
    return render(request, 'SOA/soaindex.html', context)

def filter(request):
    filter_ClientName = request.GET.get('filter_ClientName')
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')

    test1 = SOA.objects.all()

    if filter_ClientName:
        test1 = test1.filter(ClientName=filter_ClientName)
    if filter_newstatus:
        test1 = test1.filter(newstatus=filter_newstatus)
    if filter_currency1:
        test1 = test1.filter(currency1=filter_currency1)

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
        'filter_ClientName': filter_ClientName,
        'filter_newstatus': filter_newstatus,
        'filter_currency1': filter_currency1,
        'total_rows':int(total_rows),
    }
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'SOA/filter.html', context)


def delete(request, data_id):
    try:
        data = SOA.objects.get(pk=data_id)
    except SOA.DoesNotExist:
        return JsonResponse({'error': 'Row not found.'}, status=404)

    if request.method == "DELETE":
        with transaction.atomic():
            # Delete the row from the database
            data.delete()

            # Return a success response
            return JsonResponse({'message': 'Row deleted successfully.'}, status=200)

    context = {
        'test1': data
    }
    return JsonResponse(context)







def update(request, data_id):
    data = get_object_or_404(SOA, pk=data_id)
    if request.method == 'POST':
        form = SOAForm(request.POST, instance=data)

        if form.is_valid():
            form.save()
            return redirect('Accounts:index')
    else:
        form = SOAForm(instance=data)
        
    shipname_data = SOA.objects.exclude(Shipname__exact='').order_by('Shipname').values_list('Shipname', flat=True).distinct()
    ClientGroup = SOA.objects.exclude(ClientGroup__exact='').order_by('ClientGroup').values_list('ClientGroup', flat=True).distinct()
    ClientName = SOA.objects.exclude(ClientName__exact='').order_by('ClientName').values_list('ClientName', flat=True).distinct()
    POIssuedby = SOA.objects.exclude(POIssuedby__exact='').order_by('POIssuedby').values_list('POIssuedby', flat=True).distinct()
    paymentstatus = SOA.objects.exclude(paymentstatus__exact='').order_by('paymentstatus').values_list('paymentstatus', flat=True).distinct()
    newstatus  = SOA.objects.exclude(newstatus__exact='').order_by('newstatus').values_list('newstatus', flat=True).distinct()
    Branch = SOA.objects.exclude(Branch__exact='').order_by('Branch').values_list('Branch', flat=True).distinct()
    GstScope = SOA.objects.exclude(GstScope__exact='').order_by('GstScope').values_list('GstScope', flat=True).distinct()
    currency1 = SOA.objects.exclude(currency1__exact='').order_by('currency1').values_list('currency1', flat=True).distinct()
   
    
    context = {
        'form': form,
        'data_id': data_id,
        'shipname_options': shipname_data,
        'ClientGroup_options' : ClientGroup,
        'ClientName_options' : ClientName,
        'POIssuedby_options' : POIssuedby,
        'paymentstatus_options' : paymentstatus,
        'newstatus_options' : newstatus,
        'Branch_options' : Branch,
        'GstScope_options' : GstScope,
        'currency1_options' : currency1,
    }
    return render(request, 'SOA/update.html', context)

def download(request):
    
    filter_ClientName = request.GET.get('filter_ClientName') 
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')

    test1 = SOA.objects.filter()

    if filter_ClientName:
        test1 = test1.filter(ClientName=filter_ClientName)
    if filter_newstatus:
        test1 = test1.filter(newstatus=filter_newstatus)
    if filter_currency1:
        test1 = test1.filter(currency1=filter_currency1)

    

    pdf_response = BytesIO()
    

    total_amount = 0
    # for item in test1:
    #     total_amount += float(item.Invoiceamount)

    total_amount = sum(Decimal(item.Invoiceamount) for item in test1)
    total_amount = round(total_amount, 4)
    


    def generate_header_html(page_number):
            image_path = os.path.join(settings.STATICFILES_DIRS[0], 'image', 'logo.jpg')

    # Open and resize the image
            image = Image.open(image_path)
            new_width, new_height = image.size
            new_width = int(new_width * 0.5)
            new_height = int(new_height * 0.5)
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    # Convert the image to base64 for embedding in HTML
            resized_image_io = BytesIO()
            resized_image.save(resized_image_io, format='JPEG')
            resized_image_base64 = base64.b64encode(resized_image_io.getvalue()).decode()

            header_html = f'<html><head><style>'
            header_html += '.header { display: flex; justify-content: space-between; align-items: center; margin-top: 20px; }'
            header_html += '.logo { max-width: 200px; }'
            header_html += '.content { flex: 1; padding: 10px; }'
            header_html += '</style></head>'
            header_html += f'<body>'
            header_html += f'<div class="header">'
            header_html += f'<div class="content">'
            header_html += f'<div>WES Marine Controls Pte Limited</div>'
            header_html += f'<div>20 Cecil Street #05-03</div>'
            header_html += f'<div>Singapore 049705</div>'
            header_html += f'<div>GST Registered No: <span style="font-weight: bold;">202018019H</span></div>'
            header_html += f'<div>Phone: +65 69110552</div>'
            header_html += f'<div>Email: sales@wesmarines.com</div>'
            header_html += f'</div>'
            header_html += f'<div class="logo">'
            header_html += f'<img src="data:image/jpeg;base64,{resized_image_base64}" alt="Logo">'
            header_html += f'</div>'
            header_html += f'</div>'
            header_html += f'</body></html>'

            if page_number > 1:
                header_html = f'<div style="page-break-before: always;"></div>' + header_html

            return header_html

    def generate_footer_html(page_number, total_pages):
        footer_html = f'<div style="position: fixed; bottom: 20px; width: 100%; text-align: center; font-size: 12px;">(c) - page {page_number} of {total_pages}</div>'
        if page_number < total_pages:
            footer_html += f'<div></div>'
        return footer_html
    def generate_filtered_data_html(page_data,page_number,total_pages,total_amount):
        header_style = 'background-color: #0fa6d4; padding: 2px; border: 0.5px solid #000000; font-size: 10px; text-align: center;'
        content_style = 'white-space: pre-wrap; word-wrap: break-word; border: 0.5px solid #000000; padding: 3px; font-size: 8px; text-align: center;'
        td_style = 'font-size: 8px;'
        totalamount = 'white-space: pre-wrap; word-wrap: break-word; border: 0.5px solid #000000; padding: 2px; font-size: 8px;font-weight:bold'
        content_html = '<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">'
        content_html += '<colgroup> <col style="width: 20%"> <col style="width: 10%"> <col style="width: 10%"> <col style="width: 15%"> <col style="width: 10%"> <col style="width: 10%"> <col style="width: 10%"> </colgroup>'
        content_html += f'<tr> <th style="{header_style}">PONo</th> <th style="{header_style}">Duedate</th> <th style="{header_style}">InvoiceNo</th> <th style="{header_style}">Invoiceamount</th> <th style="{header_style}">paymentstatus</th> <th style="{header_style}">Invcurrency</th> <th style="{header_style}">outstandingBalance</th> </tr>'
        for item in page_data:
            content_html += f'<tr> <td style="{content_style}  {td_style}" width="20%">{item.PONo}</td> <td style="{content_style} {td_style}" width="15%">{item.Duedate}</td> <td style="{content_style} {td_style}" width="15%">{item.InvoiceNo}</td> <td style="{content_style} {td_style}" width="15%">{item.Invoiceamount}</td> <td style="{content_style} {td_style}" width="10%">{item.paymentstatus}</td> <td style="{content_style} {td_style}" width="10%">{item.Invcurrency}</td> <td style="{content_style} {td_style}" width="15%">{item.outstandingBalance}</td> </tr>'


        if total_pages == page_number:

            content_html += f'<tr> <td colspan="3" ></td> <td id="total-invoice-amount" style="{totalamount}  {td_style}">TotalInvoiceAmount : {total_amount}</td> <td colspan="3"></td> </tr>'

            

        content_html += '</table>'
        return content_html







    rows_per_page = 15

    data_chunks = [test1[i:i + rows_per_page] for i in range(0, len(test1), rows_per_page)]

    total_rows = len(test1)
    total_pages, remaining_rows = divmod(total_rows, rows_per_page)
    if remaining_rows > 0:
        total_pages += 1

    html = f'<html><head><style>@page {{ size: A4; margin: 0.35cm; }} </style></head><body>'
    for page_number, chunk in enumerate(data_chunks, start=1):
        html += generate_header_html(page_number)
        html += generate_filtered_data_html(chunk,page_number,total_pages,total_amount)
        html += generate_footer_html(page_number, total_pages)

    html += '</body></html>'

    html1 = f'<html><head><style>@page {{ size: A4; margin: 0.35cm; }} </style></head><body>'
    for page_number, chunk in enumerate(data_chunks, start=1):
        html1 += ''
        html1 += ''
        html1 += ''

    html1 += '</body></html>'
    pisa_status = pisa.CreatePDF(html1, dest=pdf_response)

    if pisa_status.err:
        return HttpResponse('PDF generation error')

    pdf_response.seek(0)
    response = HttpResponse(pdf_response.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    return response

def add(request):
    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('Accounts:index')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = SOAForm()

    shipname_data = SOA.objects.exclude(Shipname__exact='').order_by('Shipname').values_list('Shipname', flat=True).distinct()
    ClientGroup = SOA.objects.exclude(ClientGroup__exact='').order_by('ClientGroup').values_list('ClientGroup', flat=True).distinct()
    ClientName = SOA.objects.exclude(ClientName__exact='').order_by('ClientName').values_list('ClientName', flat=True).distinct()
    POIssuedby = SOA.objects.exclude(POIssuedby__exact='').order_by('POIssuedby').values_list('POIssuedby', flat=True).distinct()
    paymentstatus = SOA.objects.exclude(paymentstatus__exact='').order_by('paymentstatus').values_list('paymentstatus', flat=True).distinct() 
    newstatus  = SOA.objects.exclude(newstatus__exact='').order_by('newstatus').values_list('newstatus', flat=True).distinct()
    Branch = SOA.objects.exclude(Branch__exact='').order_by('Branch').values_list('Branch', flat=True).distinct()
    GstScope = SOA.objects.exclude(GstScope__exact='').order_by('GstScope').values_list('GstScope', flat=True).distinct()
    currency1 = SOA.objects.exclude(currency1__exact='').order_by('currency1').values_list('currency1', flat=True).distinct()
    last_id = SOA.objects.last().id if SOA.objects.exists() else 0
    context = {'last_id': last_id + 1} 
      

    context = {
        'form': form,
        'shipname_options': shipname_data,
        'ClientGroup_options' : ClientGroup,
        'ClientName_options' : ClientName,
        'POIssuedby_options' : POIssuedby,
        'paymentstatus_options' : paymentstatus,
        'newstatus_options' : newstatus,
        'Branch_options' : Branch,
        'GstScope_options' : GstScope,
        'currency1_options' : currency1,
        'last_id': last_id + 1

    }
    return render(request, 'SOA/add.html', context)

def download_csv(request):
    filter_ClientName = request.GET.get('filter_ClientName')
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')


    filters = {}
    if filter_ClientName:
        filters['ClientName'] = filter_ClientName
    if filter_newstatus:
        filters['newstatus'] = filter_newstatus
    if filter_currency1:
        filters['currency1'] = filter_currency1

    test1 = SOA.objects.filter(**filters)  # Apply the filters to the queryset

    # Define the desired fields for the CSV file
    fields = ['PONo', 'ClientName', 'InvoiceNo', 'Invoiceamount', 'paymentstatus', 'Invcurrency', 'outstandingBalance']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_data.csv"'

    writer = csv.writer(response)
    writer.writerow(fields)  

    
    for data in test1:
        row = [getattr(data, field) for field in fields]    
        writer.writerow(row)

    total_invoice_amount = sum(float(data.Invoiceamount) for data in test1)
    total_outstanding_amount = sum(float(data.outstandingBalance) for data in test1)

      # Write the "Total Invoice Amount" label and value on the same row
    writer.writerow(["Total Invoice Amount:", "", "",total_invoice_amount, "Total Outstanding Amount:", "", total_outstanding_amount])
   


    return response 

def download_full_csv(request):
    # Get all Testdata objects without applying any filters
    testdata_objects = SOA.objects.all()

    # Create the response and set the appropriate headers for CSV download
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="full_data.csv"'

    # Define the fields for the CSV file
    fields = ['id','Branch','WES_REF_NO', 'PONo', 'POIssuedby', 'ClientName', 'ClientGroup', 'Shipname', 'POAmount', 'InvoiceNo', 'InvoiceDate', 'Duedate', 'Freight', 'Invoiceamount', 'SgdValue', 'GstScope', 'currency1', 'Invamtcreditnote', 'standardrated', 'GstPaid', 'paymentstatus', 'newstatus', 'transactioncode', 'areceiveddate', 'a2ndpaymentReceiveddate', 'receivedamount', 'receivedamountCurrency', 'dc', 'discountcurrency', 'Invcurrency', 'outstandingBalance', 'supt','Dispute','DisputeReason']
    
    writer = csv.writer(response)
    writer.writerow(fields)

    # Write the data rows
    for data in testdata_objects:
        row = [getattr(data, field) for field in fields]
        writer.writerow(row)

    return response

def summary(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

   
    pivot_table = pivot(
        test1.filter(newstatus='NOT_PAID'),
        'ClientName', 'currency1', 'outstandingBalance'
    )
    pivot_table_order_processing = pivot(
        test1.filter(Q(newstatus='Orderprocessing')),
        'ClientName', 'currency1', 'outstandingBalance'
    )
    
    
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)


    # pivot_table_sorted = sorted(pivot_table, key=lambda x: x['ClientName'])
    pivot_table_sorted1 = sorted(pivot_table_order_processing, key=lambda x: x['ClientName'])
    merged_pivot_tables = pivot_table_sorted + pivot_table_sorted1
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

    inr_total1 = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted1)
    sgd_total1 = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted1)
    usd_total1 = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted1)
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount

    for item in pivot_table_sorted:
        client_name = item['ClientName'] 
        
        total_not_paid = test1.filter(ClientName=client_name, newstatus='NOT_PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='Orderprocessing').count()
        totalinvoices = total_not_paid + total_order_processing
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing

        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        'pivot_table_sorted1' : pivot_table_sorted1,
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
       
        'inr_total1': inr_total1,
        'sgd_total1': sgd_total1,
        'usd_total1': usd_total1,
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/summary.html', context)

def summary1(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

    pivot_table = pivot(
        test1.filter(newstatus='ORDER_PROCESSING'),
        'ClientName', 'currency1', 'outstandingBalance'
    )
    pivot_table_order_processing = pivot(
        test1.filter(Q(newstatus='ORDER_PROCESSING')),
        'ClientName', 'currency1', 'outstandingBalance'
    )
    


    pivot_table_sorted = sorted(pivot_table, key=lambda x: x['ClientName'])
    # pivot_table_sorted1 = sorted(pivot_table_order_processing, key=lambda x: x['ClientName'])
    pivot_table_sorted1 = sorted(pivot_table_order_processing, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    merged_pivot_tables = pivot_table_sorted + pivot_table_sorted1
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
    
    inr_total1 = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted1)
    sgd_total1 = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted1)
    usd_total1 = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted1)
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount

    for item in pivot_table_sorted:
        client_name = item['ClientName'] 
        
        total_not_paid = test1.filter(ClientName=client_name, newstatus='NOT_PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='ORDER_PROCESSING').count()
        totalinvoices = total_not_paid + total_order_processing
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing

    for item in pivot_table_sorted1:
        client_name = item['ClientName'] 
        
       
        total_order_processing1 = test1.filter(ClientName=client_name, newstatus='ORDER_PROCESSING').count()
       
       
        item['TotalOrderProcessing1'] = total_order_processing1    

        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        'pivot_table_sorted1' : pivot_table_sorted1,
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
        
        'inr_total1': inr_total1,
        'sgd_total1': sgd_total1,
        'usd_total1': usd_total1,
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
        'individialorderprocessing' :  item['TotalOrderProcessing1']  
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/summary1.html', context)

def summary2(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

    pivot_table = pivot(
        test1.filter(Q(newstatus='NOT_PAID') | Q(newstatus='ORDER_PROCESSING')),
        'ClientName', 'currency1', 'outstandingBalance'
    )
   
    pivot_table_order_processing = pivot(
        test1.filter(Q(newstatus='ORDER_PROCESSING')),
        'ClientName', 'currency1', 'outstandingBalance'
    )
   

   
    
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    pivot_table_sorted1 = sorted(pivot_table_order_processing, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    
    merged_pivot_tables = pivot_table_sorted + pivot_table_sorted1
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

    inr_total1 = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted1)
    sgd_total1 = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted1)
    usd_total1 = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted1)
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount 

    for item in pivot_table_sorted:
        client_name = item['ClientName'] 
        
        total_not_paid = test1.filter(ClientName=client_name, newstatus='NOT_PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='ORDER_PROCESSING').count()
        totalinvoices = total_not_paid + total_order_processing
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing
        total_combined = total_not_paid + total_order_processing
        
        item['TotalCombined'] = total_combined
        
        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        'pivot_table_sorted1' : pivot_table_sorted1,
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
        
        'inr_total1': inr_total1,
        'sgd_total1': sgd_total1,
        'usd_total1': usd_total1,
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
        'combined' :  item['TotalCombined']
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/summary2.html', context)

def summary3(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

    pivot_table = pivot(
        test1.filter(Q(newstatus='NOT_PAID') | Q(newstatus='ORDER_PROCESSING')),
        'Shipname', 'currency1', 'outstandingBalance'
    )
   
    pivot_table_order_processing = pivot(
        test1.filter(Q(newstatus='PAID')),
        'Shipname', 'receivedamountCurrency', 'receivedamount'
    )
    

   
    
    # pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    pivot_table_sorted1 = sorted(pivot_table_order_processing, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    
    
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

    

    for item in pivot_table_sorted:
        Shipname = item['Shipname'] 
        
        total_not_paid = test1.filter(Shipname=Shipname, newstatus='NOT_PAID').count()
        total_order_processing = test1.filter(Shipname=Shipname, newstatus='ORDER_PROCESSING').count()
        totalinvoices = total_not_paid + total_order_processing
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing
        total_combined = total_not_paid + total_order_processing
        item['TotalCombined'] = total_combined
        
        

    # grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        # 'form': form,
        # 'test1': test1,
        'pivot_table': pivot_table_sorted,
        # 'pivot_table_sorted1' : pivot_table_sorted1,
        # 'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
        
        # 'inr_total1': inr_total1,
        # 'sgd_total1': sgd_total1,
        # 'usd_total1': usd_total1,
        
        # 'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        # 'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        # 'grand_total': grand_total,
        # 'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
        'combined' :  item['TotalCombined']
             
    }

    # for item in pivot_table_sorted:   
    #     item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
    #     item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/summary3.html', context)



def paidpivotCN(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

   
    pivot_table = pivot(
        test1.filter(newstatus='PAID'),
        'ClientName', 'receivedamountCurrency', 'receivedamount'
    )
    
    
    
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)


    # pivot_table_sorted = sorted(pivot_table, key=lambda x: x['ClientName'])
    
    merged_pivot_tables = pivot_table_sorted 
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

   
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount

    for item in pivot_table_sorted:
        client_name = item['ClientName'] 
        
        total_not_paid = test1.filter(ClientName=client_name, newstatus='PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='Orderprocessing').count()
        totalinvoices = total_not_paid + total_order_processing
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing

        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
       
      
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/paidpivotCN.html', context)


def paidpivotSN(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

    pivot_table = pivot(
        test1.filter(newstatus='PAID'),
        'Shipname', 'receivedamountCurrency', 'receivedamount'
    )
    

   
    
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    
    
    merged_pivot_tables = pivot_table_sorted 
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

   
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        Shipname = item['Shipname']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[Shipname] += total_amount
        company_counts[Shipname] += 1

        item['TotalInvoiceAmount'] = total_amount 

    for item in pivot_table_sorted:
        Shipname = item['Shipname'] 
        
        total_not_paid = test1.filter(Shipname=Shipname, newstatus='PAID').count()
       
        totalinvoices = total_not_paid 
        item['TotalNotPaid'] = total_not_paid
        
        total_combined = total_not_paid 
        item['TotalCombined'] = total_combined
        
        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
        
        
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
        'combined' :  item['TotalCombined']
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount']                            
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] 


    return render(request, 'SOA/paidpivotSN.html', context)

def paidpivotCN(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

   
    pivot_table = pivot(
        test1.filter(newstatus='PAID'),
        'ClientName', 'receivedamountCurrency', 'receivedamount'
    )
    
    
    
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)


    # pivot_table_sorted = sorted(pivot_table, key=lambda x: x['ClientName'])
    
    merged_pivot_tables = pivot_table_sorted 
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

   
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount

    for item in pivot_table_sorted:
        client_name = item['ClientName'] 
        
        total_not_paid = test1.filter(ClientName=client_name, newstatus='PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='Orderprocessing').count()
        totalinvoices = total_not_paid + total_order_processing
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing

        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
       
      
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/paidpivotCN.html', context)




def wesi(request):
    form = SOAForm()

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    # Fetch all relevant data from the database
    data = SOA.objects.filter(Branch='WES-I').values('ClientName', 'newstatus', 'outstandingBalance', 'receivedamount')

    combined_pivot_table = []

    for item in data:
        client_name = item['ClientName']

        # Check if the client_name already exists in combined_pivot_table
        existing_client = next(
            (client for client in combined_pivot_table if client['ClientName'] == client_name), None)

        if existing_client:
            # Update the existing client's data
            if item['newstatus'] == 'NOT_PAID':
                existing_client['NOT_PAID'] += float(item['outstandingBalance']) if item['outstandingBalance'] else 0
            elif item['newstatus'] == 'PAID':
                existing_client['PAID'] += float(item['receivedamount']) if item['receivedamount'] else 0
        else:
            # Append a new client entry
            client_data = {
                'ClientName': client_name,
                'NOT_PAID': float(item['outstandingBalance']) if item['newstatus'] == 'NOT_PAID' and item['outstandingBalance'] else 0,
                'PAID': float(item['receivedamount']) if item['newstatus'] == 'PAID' and item['receivedamount'] else 0,
            }
            combined_pivot_table.append(client_data)

    combined_pivot_table = sorted(combined_pivot_table, key=lambda x: x['NOT_PAID'],reverse=True)        
    notpaid = sum(item.get('NOT_PAID', 0) if item.get('NOT_PAID') is not None else 0 for item in combined_pivot_table)   
    paid = sum(item.get('PAID', 0) if item.get('PAID') is not None else 0 for item in combined_pivot_table) 
    context = {
        'form': form,
        'combined_pivot_table': combined_pivot_table,
        'notpaid' : notpaid,
        'paid' : paid
    }

    return render(request, 'SOA/wesi.html', context)


def wess(request):
    form = SOAForm()

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    data = SOA.objects.filter(Branch='WES-S').values('ClientName', 'newstatus', 'outstandingBalance', 'receivedamount', 'currency1', 'receivedamountCurrency')

    combined_pivot_table = []

    for item in data:
        client_name = item['ClientName'].strip().lower()

        existing_client = next(
            (client for client in combined_pivot_table if client['ClientName'].strip().lower() == client_name),
            None
        )    

        if existing_client:
            # Existing client, update counts
            if item['newstatus'] == 'NOT_PAID':
                if item['currency1'] == 'SGD':
                    existing_client['NOT_PAID_SGD'] += float(item['outstandingBalance']) if item['outstandingBalance'] else 0
                    existing_client['InvoiceCount'] += 1
                elif item['currency1'] == 'USD':
                    existing_client['NOT_PAID_USD'] += float(item['outstandingBalance']) if item['outstandingBalance'] else 0
                    existing_client['InvoiceCount'] += 1
            elif item['newstatus'] == 'ORDER_PROCESSING':
                if item['currency1'] == 'SGD':
                    existing_client['ORDER_PROCESSING_SGD'] += float(item['outstandingBalance']) if item['outstandingBalance'] else 0
                    existing_client['InvoiceCount'] += 1
                elif item['currency1'] == 'USD':
                    existing_client['ORDER_PROCESSING_USD'] += float(item['outstandingBalance']) if item['outstandingBalance'] else 0
                    existing_client['InvoiceCount'] += 1

            # Combine 'PAID' statuses
            elif item['newstatus'] == 'PAID':
                if item['receivedamountCurrency'] == 'SGD':
                    existing_client['PAID_SGD'] += float(item['receivedamount']) if item['receivedamount'] else 0
                    existing_client['InvoiceCount'] += 1
                if item['receivedamountCurrency'] == 'USD':
                    existing_client['PAID_USD'] += float(item['receivedamount']) if item['receivedamount'] else 0
                    existing_client['InvoiceCount'] += 1
                if item['receivedamountCurrency'] == 'INR':
                    existing_client['PAID_INR'] += float(item['receivedamount']) if item['receivedamount'] else 0  
                    existing_client['InvoiceCount'] += 1 

            # Increment the invoice count
            # existing_client['InvoiceCount'] += 1
        else:
            # New client, initialize counts and invoice count
            not_paid_sgd = float(item['outstandingBalance']) if item['newstatus'] == 'NOT_PAID' and item['currency1'] == 'SGD' and item['outstandingBalance'] else 0
            not_paid_usd = float(item['outstandingBalance']) if item['newstatus'] == 'NOT_PAID' and item['currency1'] == 'USD' and item['outstandingBalance'] else 0
            order_processing_sgd = float(item['outstandingBalance']) if item['newstatus'] == 'ORDER_PROCESSING' and item['currency1'] == 'SGD' and item['outstandingBalance'] else 0
            order_processing_usd = float(item['outstandingBalance']) if item['newstatus'] == 'ORDER_PROCESSING' and item['currency1'] == 'USD' and item['outstandingBalance'] else 0
            paid_sgd = float(item['receivedamount']) if item['newstatus'] == 'PAID' and item['receivedamountCurrency'] == 'SGD' and item['receivedamount'] else 0
            paid_usd = float(item['receivedamount']) if item['newstatus'] == 'PAID' and item['receivedamountCurrency'] == 'USD' and item['receivedamount'] else 0
            paid_inr = float(item['receivedamount']) if item['newstatus'] == 'PAID' and item['receivedamountCurrency'] == 'INR' and item['receivedamount'] else 0
            
            client_data = {
                'ClientName': item['ClientName'],
                'NOT_PAID_SGD': not_paid_sgd,
                'NOT_PAID_USD': not_paid_usd,
                'ORDER_PROCESSING_SGD': order_processing_sgd,
                'ORDER_PROCESSING_USD': order_processing_usd,
                'PAID_SGD': paid_sgd,
                'PAID_USD': paid_usd,
                'PAID_INR':paid_inr,
                'InvoiceCount': 1
            }
            combined_pivot_table.append(client_data)

    combined_pivot_table = sorted(combined_pivot_table, key=lambda x: x['ClientName'])
    total_invoice_count = sum(item['InvoiceCount'] for item in combined_pivot_table)
    notpaid_sgd = sum(item.get('NOT_PAID_SGD', 0) for item in combined_pivot_table)
    notpaid_usd = sum(item.get('NOT_PAID_USD', 0) for item in combined_pivot_table)
    order_processing_sgd = sum(item.get('ORDER_PROCESSING_SGD', 0) for item in combined_pivot_table)
    order_processing_usd = sum(item.get('ORDER_PROCESSING_USD', 0) for item in combined_pivot_table)
    paid_sgd = sum(item.get('PAID_SGD', 0) for item in combined_pivot_table)
    paid_usd = sum(item.get('PAID_USD', 0) for item in combined_pivot_table)
    paid_inr = sum(item.get('PAID_INR', 0) for item in combined_pivot_table)

    context = {
        'form': form,
        'combined_pivot_table': combined_pivot_table,
        'notpaid_sgd': notpaid_sgd,
        'notpaid_usd': notpaid_usd,
        'order_processing_sgd': order_processing_sgd,
        'order_processing_usd': order_processing_usd,
        'paid_sgd': paid_sgd,
        'paid_usd': paid_usd,
        'paid_inr':paid_inr,
        'total_invoice_count': total_invoice_count
    }

    return render(request, 'SOA/wess.html', context)

                  
def addnew(request):
    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('Accounts:index')
            except Exception as e:
                return HttpResponse(f"An error occurred: {str(e)}")
        else:
            return HttpResponse("Form is not valid.")
    else:
        form = SOAForm()

    shipname_data = SOA.objects.exclude(Shipname__exact='').order_by('Shipname').values_list('Shipname', flat=True).distinct()
    ClientGroup = SOA.objects.exclude(ClientGroup__exact='').order_by('ClientGroup').values_list('ClientGroup', flat=True).distinct()
    ClientName = SOA.objects.exclude(ClientName__exact='').order_by('ClientName').values_list('ClientName', flat=True).distinct()
    POIssuedby = SOA.objects.exclude(POIssuedby__exact='').order_by('POIssuedby').values_list('POIssuedby', flat=True).distinct()
    paymentstatus = SOA.objects.exclude(paymentstatus__exact='').order_by('paymentstatus').values_list('paymentstatus', flat=True).distinct() 
    newstatus  = SOA.objects.exclude(newstatus__exact='').order_by('newstatus').values_list('newstatus', flat=True).distinct()
    Branch = SOA.objects.exclude(Branch__exact='').order_by('Branch').values_list('Branch', flat=True).distinct()
    GstScope = SOA.objects.exclude(GstScope__exact='').order_by('GstScope').values_list('GstScope', flat=True).distinct()
    currency1 = SOA.objects.exclude(currency1__exact='').order_by('currency1').values_list('currency1', flat=True).distinct()
    last_id = SOA.objects.last().id if SOA.objects.exists() else 0
    context = {'last_id': last_id + 1} 
      

    context = {
        'form': form,
        'shipname_options': shipname_data,
        'ClientGroup_options' : ClientGroup,
        'ClientName_options' : ClientName,
        'POIssuedby_options' : POIssuedby,
        'paymentstatus_options' : paymentstatus,
        'newstatus_options' : newstatus,
        'Branch_options' : Branch,
        'GstScope_options' : GstScope,
        'currency1_options' : currency1,
        'last_id': last_id + 1

    }
    return render(request, 'SOA/addnew.html', context)



def dispute(request):
    filter_ClientName = request.GET.get('filter_ClientName')
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')

    test1 = SOA.objects.all()
    test1 = test1.filter(Dispute = 'Yes')

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
        'filter_ClientName': filter_ClientName,
        'filter_newstatus': filter_newstatus,
        'filter_currency1': filter_currency1,
        'total_rows':int(total_rows) ,
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'SOA/dispute.html', context)

def disputeold(request):
    filter_ClientName = request.GET.get('filter_ClientName')
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')

    test1 = SOA.objects.all()
    test1 = test1.filter(Dispute = 'Old')

    filtered_data = list(test1.values())    
    total_rows = len(filtered_data)
    context = {
        'test1': test1,
        'filter_ClientName': filter_ClientName,
        'filter_newstatus': filter_newstatus,
        'filter_currency1': filter_currency1,
        'total_rows':int(total_rows) ,
    }
    # return JsonResponse({'total_rows': total_rows})
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return JsonResponse(filtered_data, safe=False)
    
    return render(request,'SOA/disputeold.html', context)









def clientname(request):
    form = SOAForm()

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

    test1 = SOA.objects.annotate(
        sum_fields=ExpressionWrapper(
            F('outstandingBalance') + F('receivedamount'),
            output_field=IntegerField()
        )
    )

    # Create the pivot table based on the calculated 'sum_fields'
    pivot_table = pivot(
        test1.filter(Q(newstatus='NOT_PAID') | Q(newstatus='ORDER_PROCESSING') | Q(newstatus='PAID')),
        'ClientName', 'currency1', 'sum_fields'
    )




    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    # pivot_table_sorted1 = sorted(pivot_table_order_processing, key=lambda x: x.get('USD', 0) or 0, reverse=True)

    merged_pivot_tables = pivot_table_sorted

    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)


    # inr_total1 = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted1)
    # sgd_total1 = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted1)
    # usd_total1 = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted1)


    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount

    for item in pivot_table_sorted:
        client_name = item['ClientName']

        total_not_paid = test1.filter(ClientName=client_name, newstatus='NOT_PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='ORDER_PROCESSING').count()
        total_paid = test1.filter(ClientName=client_name, newstatus='PAID').count()
        totalinvoices = total_not_paid + total_order_processing + total_paid
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing
        item['TotalPAID'] = total_paid
        total_combined = total_not_paid + total_order_processing + total_paid

        item['TotalCombined'] = total_combined



    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted) +sum(item['TotalPAID'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        # 'pivot_table_sorted1' : pivot_table_sorted1,
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,


        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total': total,
        'combined' :  item['TotalCombined']

    }

    for item in pivot_table_sorted:
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing']


    return render(request, 'SOA/clientname.html', context)

def shipname(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

    test1 = SOA.objects.annotate(
        sum_fields=ExpressionWrapper(
            F('outstandingBalance') + F('receivedamount'),
            output_field=IntegerField()
        )
    )

    # Create the pivot table based on the calculated 'sum_fields'
    pivot_table = pivot(
        test1.filter(Q(newstatus='NOT_PAID') | Q(newstatus='ORDER_PROCESSING') | Q(newstatus='PAID')),
        'Shipname', 'currency1', 'sum_fields'  
    )
    

   
    
    # pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)
    
    merged_pivot_tables = pivot_table_sorted 
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

    # inr_total1 = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted1)
    # sgd_total1 = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted1)
    # usd_total1 = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted1)
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        Shipname = item['Shipname']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[Shipname] += total_amount
        company_counts[Shipname] += 1

        item['TotalInvoiceAmount'] = total_amount 

    for item in pivot_table_sorted:
        Shipname = item['Shipname'] 
        
        total_not_paid = test1.filter(Shipname=Shipname, newstatus='NOT_PAID').count()
        total_order_processing = test1.filter(Shipname=Shipname, newstatus='ORDER_PROCESSING').count()
        total_paid = test1.filter(Shipname=Shipname, newstatus='PAID').count()
        totalinvoices = total_not_paid + total_order_processing + total_paid
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing
        item['TotalPAID'] = total_paid
        total_combined = total_not_paid + total_order_processing + total_paid
        item['TotalCombined'] = total_combined
        
        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted) + sum(item['TotalPAID'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        # 'pivot_table_sorted1' : pivot_table_sorted1,
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
               
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
        'combined' :  item['TotalCombined']
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']  + item['TotalPAID']                              
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] + item['TotalPAID']


    return render(request, 'SOA/shipname.html', context)


def disputecsv(request):
    # Fetch the filtered data where Dispute is "Yes"
    filtered_data = SOA.objects.filter(Dispute="Yes")

    # Define the desired fields for the CSV file
    fields = ['PONo', 'ClientName', 'InvoiceNo', 'Invoiceamount', 'paymentstatus', 'Invcurrency', 'outstandingBalance','DisputeReason']

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="disputed_data.csv"'

    writer = csv.writer(response)
    writer.writerow(fields)  # Write the header row

    # Write the data rows
    for data in filtered_data:
        row = [getattr(data, field) for field in fields]    
        writer.writerow(row)

    return response

def test(request):

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()
            filter_ClientName = form.cleaned_data['ClientName']
            filter_newstatus = form.cleaned_data['newstatus']
            filter_currency1 = form.cleaned_data['currency1']
            url = reverse('Accounts:filter')
            url += f'?filter_ClientName={filter_ClientName}&filter_newstatus={filter_newstatus}&filter_currency1={filter_currency1}'
            return HttpResponseRedirect(url)
    else:
        form = SOAForm()


    if request.GET.get('filter_ClientName'):
        filter_ClientName1 = request.GET.get('filter_ClientName')
        
        
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            
            return JsonResponse({'message': 'Filtered data'})
    test1 = SOA.objects.all()
  

    filter_ClientName = request.GET.get('filter_ClientName')
    filter_newstatus = request.GET.get('filter_newstatus')
    filter_currency1 = request.GET.get('filter_currency1')
    
    if filter_ClientName:
        test1 = test1.filter(ClientName=filter_ClientName)
    if filter_newstatus:
        test1 = test1.filter(newstatus=filter_newstatus)
    if filter_currency1:
        test1 = test1.filter(currency1=filter_currency1)

    unique_clients = SOA.objects.order_by('ClientName').values_list('ClientName', flat=True).distinct()
    unique_newstatuses = SOA.objects.order_by('newstatus').values_list('newstatus', flat=True).distinct()
    unique_currencies = SOA.objects.order_by('currency1').values_list('currency1', flat=True).distinct()
        

    context = {
        'form': form,
        'test1': test1,
        'filter_ClientName': filter_ClientName,
        'filter_newstatus': filter_newstatus,
        'filter_currency1': filter_currency1,
        'unique_clients': unique_clients,
        'unique_newstatuses': unique_newstatuses,  
        'unique_currencies': unique_currencies,   
    }
    return render(request, 'SOA/test.html',context)



def discount(request):
    form = SOAForm() 

    if request.method == "POST":
        form = SOAForm(request.POST)
        if form.is_valid():
            form.save()

    test1 = SOA.objects.all()

   
    pivot_table = pivot(
        test1.filter(newstatus='PAID'),
        'ClientName', 'discountcurrency', 'dc'
    )
    
    
    
    pivot_table_sorted = sorted(pivot_table, key=lambda x: x.get('USD', 0) or 0, reverse=True)


    # pivot_table_sorted = sorted(pivot_table, key=lambda x: x['ClientName'])
    
    merged_pivot_tables = pivot_table_sorted 
    
    inr_total = sum(item.get('INR', 0) if item.get('INR') is not None else 0 for item in pivot_table_sorted)
    sgd_total = sum(item.get('SGD', 0) if item.get('SGD') is not None else 0 for item in pivot_table_sorted)
    usd_total = sum(item.get('USD', 0) if item.get('USD') is not None else 0 for item in pivot_table_sorted)
   

   
    

    total_amounts = defaultdict(float)
    company_counts = defaultdict(int)

    for item in pivot_table:
        client_name = item['ClientName']
        inr = item.get('INR', 0) or 0
        sgd = item.get('SGD', 0) or 0
        usd = item.get('USD', 0) or 0
        blank = item.get('BLANK', 0) or 0
        total_amount = inr + sgd + usd + blank

        total_amounts[client_name] += total_amount
        company_counts[client_name] += 1

        item['TotalInvoiceAmount'] = total_amount

    for item in pivot_table_sorted:
        client_name = item['ClientName'] 
        
        total_not_paid = test1.filter(ClientName=client_name, newstatus='PAID').count()
        total_order_processing = test1.filter(ClientName=client_name, newstatus='Orderprocessing').count()
        totalinvoices = total_not_paid 
        item['TotalNotPaid'] = total_not_paid
        item['TotalOrderProcessing'] = total_order_processing

        

    grand_total = sum(item['TotalInvoiceAmount'] for item in pivot_table_sorted)
    total_not_paid_order_processing = sum(item['TotalNotPaid'] for item in pivot_table_sorted) + sum(item['TotalOrderProcessing'] for item in pivot_table_sorted)
    context = {
        'form': form,
        'test1': test1,
        'pivot_table': pivot_table_sorted,
        
        'merged_pivot_tables' : merged_pivot_tables,
        'inr_total': inr_total,
        'sgd_total': sgd_total,
        'usd_total': usd_total,
       
      
        
        'total_not_paid': sum(item['TotalNotPaid'] for item in pivot_table_sorted),
        'total_order_processing': sum(item['TotalOrderProcessing'] for item in pivot_table_sorted),
        'grand_total': grand_total,
        'totalinvoices' : totalinvoices,
        'total_not_paid_order_processing': total_not_paid_order_processing,
             
    }

    for item in pivot_table_sorted:   
        item['TotalInvoiceAmountOrderProcessing'] = item['TotalInvoiceAmount'] + item['TotalOrderProcessing']                                
        item['TotalNotPaidOrderProcessing'] = item['TotalNotPaid'] + item['TotalOrderProcessing'] 


    return render(request, 'SOA/discount.html', context)

