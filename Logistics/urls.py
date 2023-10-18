from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Logistics'

urlpatterns = [ 

    
   
    path('logindex/', views.logindex, name='logindex'),
    path('dhl/', views.dhl, name='dhl'),
    path('dhlindex/', views.dhlindex, name='dhlindex'),
    path('dhlexcel/', views.dhlexcel, name='dhlexcel'),
    path('adddhl/', views.adddhl, name='adddhl'),
    path('addnewdhl/', views.addnewdhl, name='addnewdhl'),
    path('updatedhl/<int:data_id>/', views.updatedhl, name='updatedhl'),
    path('get-dropdown-options1/', views.get_dropdown_options1, name='get_dropdown_options1'),
    path('get-dropdown-optionstocountry/', views.get_dropdown_optionstocountry, name='get_dropdown_optionstocountry'),
    path('commercialinvoice/', views.commercialinvoice, name='commercialinvoice'), 
    path('dodnnumber/', views.dodnnumber, name='dodnnumber'), 
    path('wesnewsg/', views.wesnewsg, name='wesnewsg'), 
    path('addci/', views.addci, name='addci'), 
    path('addnewci/', views.addnewci, name='addnewci'), 
    path('commercialinvoiceci/', views.commercialinvoiceci, name='commercialinvoiceci'), 
    path('adddn/', views.adddn, name='adddn'), 
    path('addnewdn/', views.addnewdn, name='addnewdn'), 
    path('dodnnumberdn/', views.dodnnumberdn, name='dodnnumberdn'), 
    path('addwns/', views.addwns, name='addwns'), 
    path('addnewwns/', views.addnewwns, name='addnewwns'), 
    path('wesnewsgwns/', views.wesnewsgwns, name='wesnewsgwns'), 
    path('updateci/<int:data_id>/', views.updateci, name='updateci'), 
    path('updatedn/<int:data_id>/', views.updatedn, name='updatedn'), 
    path('updatewns/<int:data_id>/', views.updatewns, name='updatewns'), 
    path('addci/', views.addci, name='addci'), 
    path('addnewci/', views.addnewci, name='addnewci'), 
    path('commercialinvoice/', views.commercialinvoice, name='commercialinvoice'),
    # path('commercialpacl/', views.commercialpacl, name='commercialpacl'),
    path('updateci/<int:data_id>/', views.updateci, name='updateci'), 
    path('wessindex/', views.wessindex, name='wessindex'), 
    path('wesiindex/', views.wesiindex, name='wesiindex'), 
    path('download_ci_csv/', views.download_ci_csv, name='download_ci_csv'), 
    path('download_dodnnumber_csv/', views.download_dodnnumber_csv, name='download_dodnnumber_csv'), 
    path('download_wesnewsg_csv/', views.download_wesnewsg_csv, name='download_wesnewsg_csv'), 
     path('addcp/', views.addcp, name='addcp'), 
    path('addnewcp/', views.addnewcp, name='addnewcp'), 
    path('commercialpaclcp/', views.commercialpaclcp, name='commercialpaclcp'),
    path('commercialpacl/', views.commercialpacl, name='commercialpacl'),
    path('updatecp/<int:data_id>/', views.updatecp, name='updatecp'), 
    path('addin/', views.addin, name='addin'), 
    path('addnewin/', views.addnewin, name='addnewin'), 
    path('invoicenumberin/', views.invoicenumberin, name='invoicenumberin'),
    path('invoicenumber/', views.invoicenumber, name='invoicenumber'),
    path('updatein/<int:data_id>/', views.updatein, name='updatein'), 
    path('adddo/', views.adddo, name='adddo'), 
    path('addnewdo/', views.addnewdo, name='addnewdo'), 
    path('donumberdo/', views.donumberdo, name='donumberdo'),
    path('donumber/', views.donumber, name='donumber'),
    path('updatedo/<int:data_id>/', views.updatedo, name='updatedo'), 
    path('addp/', views.addp, name='addp'), 
    path('addnewp/', views.addnewp, name='addnewp'), 
    path('proformap/', views.proformap, name='proformap'),
    path('proforma/', views.proforma, name='proforma'),
    path('updatep/<int:data_id>/', views.updatep, name='updatep'),
    path('download_ci_csv/', views.download_ci_csv, name='download_ci_csv'), 
    path('download_dodnnumber_csv/', views.download_dodnnumber_csv, name='download_dodnnumber_csv'), 
    path('download_wesnewsg_csv/', views.download_wesnewsg_csv, name='download_wesnewsg_csv'), 
    path('download_commercial_Pacl_csv/', views.download_commercial_Pacl_csv, name='download_commercial_Pacl_csv'), 
    path('download_Invoice_Number_csv/', views.download_Invoice_Number_csv, name='download_Invoice_Number_csv'), 
    path('download_Do_Number_csv/', views.download_Do_Number_csv, name='download_Do_Number_csv'), 
    path('download_Proforma_csv/', views.download_Proforma_csv, name='download_Proforma_csv'), 
   
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)