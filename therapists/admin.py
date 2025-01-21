from django.contrib import admin
from .models import Therapist, TherapistService
from core.models import AcceptedCustomerGroups


@admin.register(Therapist)
class TherapistAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'gender', 'age', 'street', 'number', 'postcode', 'city', 'country', 
                    'phone_number', 'years_xp', 'pronouns', 'accepted_customer_groups_display')
    search_fields = ('first_name', 'last_name', 'user__username', 'street', 'city', 'phone_number')
    list_filter = ('first_name', 'last_name', 'gender', 'years_xp', 'city', 'country')
    ordering = ('first_name', 'last_name')

    #Displays the accepted customer groups as a readable string.
    def accepted_customer_groups_display(self, obj):
        return ", ".join(obj.accepted_customer_groups)     

    accepted_customer_groups_display.short_description = 'Accepted Customer Groups'


@admin.register(AcceptedCustomerGroups)
class AcceptedCustomerGroupsAdmin(admin.ModelAdmin):
    list_display = ('choice',)


@admin.register(TherapistService)
class TherapistServiceAdmin(admin.ModelAdmin):
    list_display = ('therapist', 'service', 'base_price')
    search_fields = ('therapist__first_name', 'therapist__last_name', 'service__name')
    list_filter = ('therapist__first_name', 'therapist__last_name', 'service__name')
