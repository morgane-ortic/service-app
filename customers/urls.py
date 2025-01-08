from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'customers'

urlpatterns = [
    path('services/', views.services, name='services'),
    path('bookings/', views.bookings, name='bookings'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
