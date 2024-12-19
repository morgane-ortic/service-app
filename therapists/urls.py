from django.urls import path
from . import views

app_name = 'therapists'

urlpatterns = [
    path('', views.home, name='home'),
    path('notifications/', views.notifications, name='notifications'),
    path('schedule', views.schedule, name='schedule'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('customer_profile', views.customer_profile, name='customer_profile'),
]