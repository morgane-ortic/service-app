from django.contrib import admin
from .models import Service

# Register the Service model
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'description')  # Fields to display in the admin list view
    search_fields = ('name', 'description')  # Add a search box for these fields
