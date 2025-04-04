from django.urls import path
from . import views
import core.views

app_name = 'therapists'

urlpatterns = [
    path('', views.home, name='home'),
    path('notifications/', core.views.display_notifications, name='notifications'),
    path('schedule/', views.schedule, name='schedule'),
    
    path('profile/<str:section>/', views.profile, name='profile'),
    path('profile/delete_service/<int:therapist_id>/<int:service_id>/', views.delete_service, name='delete_service'),
    path('profile/', views.profile, name='profile_default'),

    path('about/', views.about, name='about'),

    path('register/', views.register, name='register'),
    path('register_details/', views.register_details, name='register_details'),
    path('logout/', views.user_logout, name='logout'),

    path('customer_profile/', views.customer_profile, name='customer_profile'),

    path('get_notifications/', core.views.get_notifications, name='get_notifications'),
]