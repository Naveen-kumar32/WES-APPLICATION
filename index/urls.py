from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'index'

urlpatterns = [ 

    path('signup/', views.signup, name='signup'),
    path('', views.user_login, name='login'),  # Fix the path for the login view to be an empty string
    
     
    path('logout/', views.user_logout, name='logout'),
    path('user/<int:user_id>/', views.master, name='master'),
    path('user/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    
    path('updatelogin/', views.updatelogin, name='updatelogin'),
    
    
    
    
] 
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)