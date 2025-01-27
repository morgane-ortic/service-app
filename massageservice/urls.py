from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
import customers.views
import core.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', core.views.user_login, name='login'),
    path('customers/', include('customers.urls', namespace='customers')),
    path('therapists/', include('therapists.urls', namespace='therapists')),
    path('success/', customers.views.payment_success, name='success'),  # Add the success endpoint
    path('cancel/', customers.views.payment_cancel, name='cancel'),     # Add the cancel endpoint

    path('get_notifications/', core.views.get_notifications, name='get_notifications'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)