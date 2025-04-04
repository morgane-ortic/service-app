from django.urls import path
from . import views
from .views import create_checkout_session
from django.contrib.auth import views as auth_views
from .views import payment_success, payment_cancel
from django.http import HttpResponse
import core.views

app_name = 'customers'

urlpatterns = [
    path('', views.home, name='home'),
    path('notifications/', core.views.display_notifications, name='notifications'),
    path('services/', views.services, name='services'),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('bookings/', views.bookings, name='bookings'),
    path("cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("get-addresses/", views.get_addresses, name="get_addresses"),
    path("get-current-booking/", views.get_current_booking, name="get_current_booking"),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('register_details/', views.register_details, name='register_details'),
    path('logout/', views.user_logout, name='logout'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),

    path('get-notifications/', core.views.get_notifications, name='get_notifications'),

    path('favicon.ico', lambda x: HttpResponse(status=204)),  # Ignore favicon requests
]
