from django.contrib import admin
from .models import Service
from .models import Booking

# Register the Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'description')  # Fields to display in the admin list view
    search_fields = ('name', 'description')  # Add a search box for these fields

# Register the Booking model
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'therapist', 'service', 'number_of_customers', 'booking_date_time', 'price', 'created_at')
    list_filter = ('booking_date_time', 'therapist', 'service')
    search_fields = ('customer__user__username', 'therapist__user__username', 'address')