from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender')
    search_fields = ('user__username', 'name')
    list_filter = ('gender',)

    # Add any additional customization if needed