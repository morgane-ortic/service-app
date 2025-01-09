from django.shortcuts import render, get_object_or_404
from core.models import Service, ServiceType
from django.conf import settings

# Placeholder views
def home(request):
    return render(request, 'customers/home.html')

def services(request):
    return render(request, 'customers/services.html')


def bookings(request):
    service_type_name = request.GET.get('service_type', 'all')
    if service_type_name == 'all':
        services = Service.objects.all()
    else:
        try:
            service_type = ServiceType.objects.get(name=service_type_name)
            services = Service.objects.filter(service_types=service_type)
        except ServiceType.DoesNotExist:
            services = Service.objects.none()

    service_types = ServiceType.objects.all()

    return render(request, 'customers/bookings.html', {
        'services': services,
        'service_types': service_types,
        'selected_type': service_type_name,
    })

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    return render(request, 'customers/service_detail.html', {'service': service})



def profile(request):
    return render(request, 'customers/profile.html')

def about(request):
    print(settings.TEMPLATES[0]['DIRS'])
    return render(request, 'core/about.html', {
        'base_template': 'customers/base.html'
    })

def contact(request):
    return render(request, 'core/contact.html', {
        'base_template': 'customers/base.html'
    })

def register(request):
    return render(request, 'customers/register.html')

def login(request):
    return render(request, 'core/login.html', {
        'base_template': 'customers/base.html'
    })