from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'index'

urlpatterns = [ 

    path('', views.loginindex, name='loginindex'),
    path('Accountslogin/', views.Accountslogin, name='Accountslogin'),
    path('Procurement/', views.Procurement, name='Procurement'),
    path('Logistics/', views.Logistics, name='Logistics'),
    path('Management/', views.Management, name='Management'),
    path('Viewonly/', views.Viewonly, name='Viewonly'),
    
    
    
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)