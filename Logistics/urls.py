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
    path('get-dropdown-options1/', views.get_dropdown_options1, name='get_dropdown_options1'),
    path('get-dropdown-optionstocountry/', views.get_dropdown_optionstocountry, name='get_dropdown_optionstocountry'),
    path('addnewdhl/', views.addnewdhl, name='addnewdhl'),
    path('updatedhl/<int:data_id>/', views.updatedhl, name='updatedhl'), 
    path('commercialinvoice/', views.commercialinvoice, name='commercialinvoice'), 
    path('dodnnumber/', views.dodnnumber, name='dodnnumber'), 
    path('addci/', views.addci, name='addci'), 
    path('addnewci/', views.addnewci, name='addnewci'), 
    path('commercialinvoiceci/', views.commercialinvoiceci, name='commercialinvoiceci'), 
    path('adddn/', views.adddn, name='adddn'), 
    path('addnewdn/', views.addnewdn, name='addnewdn'), 
    path('dodnnumberdn/', views.dodnnumberdn, name='dodnnumberdn'), 
    path('updateci/<int:data_id>/', views.updateci, name='updateci'), 
    path('updatedn/<int:data_id>/', views.updatedn, name='updatedn'), 
    path('addcp/', views.addcp, name='addcp'), 
    path('addnewcp/', views.addnewcp, name='addnewcp'), 
    path('commercialpaclcp/', views.commercialpaclcp, name='commercialpaclcp'),
    path('commercialpacl/', views.commercialpacl, name='commercialpacl'),
    path('updatecp/<int:data_id>/', views.updatecp, name='updatecp'), 
    path('adddo/', views.adddo, name='adddo'), 
    path('addnewdo/', views.addnewdo, name='addnewdo'), 
    path('donumberdo/', views.donumberdo, name='donumberdo'),
    path('donumber/', views.donumber, name='donumber'),
    path('updatedo/<int:data_id>/', views.updatedo, name='updatedo'), 
    path('download_ci_csv/', views.download_ci_csv, name='download_ci_csv'), 
    path('download_dodnnumber_csv/', views.download_dodnnumber_csv, name='download_dodnnumber_csv'),  
    path('download_commercial_Pacl_csv/', views.download_commercial_Pacl_csv, name='download_commercial_Pacl_csv'), 
    path('download_Do_Number_csv/', views.download_Do_Number_csv, name='download_Do_Number_csv'), 
    path('ordertracking/', views.ordertracking, name='ordertracking'),
    path('dropdown_status/', views.dropdown_status, name='dropdown_status'),
    path('ordertracking_csv/', views.ordertracking_csv, name='ordertracking_csv'),
    path('tracking_csv/', views.tracking_csv, name='tracking_csv'),
    path('addtracking/', views.addtracking, name='addtracking'),
    path('addnewtracking/', views.addnewtracking, name='addnewtracking'),
    path('filterbtn/', views.filterbtn, name='filterbtn'),
    path('updatetracking/<int:data_id>/', views.updatetracking, name='updatetracking'),
    path('order/', views.order, name='order'),
    path('information/', views.information, name='information'),
    path('consignee/', views.consignee, name='consignee'),
    path('freightcost/', views.freightcost, name='freightcost'),
    path('arrangeddispatch/', views.arrangeddispatch, name='arrangeddispatch'),
    path('dispatched/', views.dispatched, name='dispatched'),
    path('delivered/', views.delivered, name='delivered'),
    path('pending/', views.pending, name='pending'),
    path('invoiced/', views.invoiced, name='invoiced'),
    path('holdpo/', views.holdpo, name='holdpo'),
    path('ongoing/', views.ongoing, name='ongoing'),
   
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)