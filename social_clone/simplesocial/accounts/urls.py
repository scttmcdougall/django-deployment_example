
#import django's path functionality from conf.urls
#from django.conf.urls import path
from django.urls import path

#login logout views are automatic (exists within Django)
from django.contrib.auth import views as auth_views

#import views from views.py
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html'),name='login'),
    #uses default view
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    #uses Signup view in views.py
    path('signup/',views.SignUp.as_view(),name='signup'),

]
