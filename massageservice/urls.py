from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from customers import views  # Import the views where `payment_success` and `payment_cancel` are defined


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('customers/', include('customers.urls', namespace='customers')),
    path('therapists/', include('therapists.urls', namespace='therapists')),
    path('success/', views.payment_success, name='success'),  # Add the success endpoint
    path('cancel/', views.payment_cancel, name='cancel'),     # Add the cancel endpoint
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)