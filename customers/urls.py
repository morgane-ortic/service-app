from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'customers'

urlpatterns = [
    path('services/', views.services, name='services'),
    path('bookings/', views.bookings, name='bookings'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('register_details/', views.register_details, name='register_details'),
    path('register_confirm/', views.register_confirm, name='register_confirm'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
]
