from django.contrib import admin
from django.urls import path, include
from customers import views as customers_views
from therapists import views as therapists_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', customers_views.home, name='home'),
    path('customers/', include('customers.urls')),
    path('therapists/', include('therapists.urls')),
]