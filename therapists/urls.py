from django.urls import path
from . import views

app_name = 'therapists'

urlpatterns = [
    path('', views.home, name='home'),
    path('notifications/', views.notifications, name='notifications'),
    path('schedule/', views.schedule, name='schedule'),
    
    path('profile/<str:section>/', views.profile, name='profile'),
    path('profile/', views.profile, name='profile_default'),

    path('about/', views.about, name='about'),

    path('register/', views.register, name='register'),
    path('register_details/', views.register_details, name='register_details'),
    path('logout/', views.user_logout, name='logout'),

    path('customer_profile/', views.customer_profile, name='customer_profile'),
]