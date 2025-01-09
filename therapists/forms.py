from django import forms
from .models import Therapist, CustomerNumber

# The field and form below are handling the multiple choices for number of customers accepted
# The form will have to be included in the views

class MultiSelectFormField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = forms.CheckboxSelectMultiple
        super().__init__(*args, **kwargs)

class TherapistForm(forms.ModelForm):
    number_of_customers = MultiSelectFormField(
        queryset=CustomerNumber.objects.all(),
        required=True
    )

    class Meta:
        model = Therapist
        fields = ['name', 'gender', 'description', 'picture', 'specialties', 'years_xp', 'number_of_customers', 'equipment_pref']