from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Accounts'

urlpatterns = [ 

    
   
    path('index/', views.index, name='index'),
    path('soaindex/', views.soaindex, name='soaindex'),
    path('delete/<int:data_id>/', views.delete, name='delete'),
    path('update/<int:data_id>/', views.update, name='update'),
    path('filter/', views.filter, name='filter'),
    path('download/', views.download, name='download'),
    path('add/', views.add, name='add'),
    path('addnew/', views.addnew, name='addnew'),
    path('download-csv/', views.download_csv, name='download-csv'),
    path('download_full_csv/', views.download_full_csv, name='download_full_csv'),
    path('summary/', views.summary, name='summary'), 
    path('summary1/', views.summary1, name='summary1'), 
    path('summary2/', views.summary2, name='summary2'),
    path('summary3/', views.summary3, name='summary3'),
    path('paidpivotCN/', views.paidpivotCN, name='paidpivotCN'),
    path('paidpivotSN/', views.paidpivotSN, name='paidpivotSN'),
    path('get-dropdown-options/', views.get_dropdown_options, name='get_dropdown_options'),
    path('get-dropdown-optionsnewstatus/', views.get_dropdown_optionsnewstatus, name='get_dropdown_optionsnewstatus'),
    path('wesi/', views.wesi, name='wesi'),
    path('wess/', views.wess, name='wess'),
    path('dispute/', views.dispute, name='dispute'),
    path('disputeold/', views.disputeold, name='disputeold'),
    path('clientname/', views.clientname, name='clientname'),
    path('shipname/', views.shipname, name='shipname'),
    path('disputecsv/', views.disputecsv, name='disputecsv'),
    path('discount/', views.discount, name='discount'), 
      
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)