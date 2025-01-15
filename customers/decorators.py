from django.shortcuts import redirect

def customer_required(view_func):
    '''if user is not logged in as a customer, redirect to homepage'''
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'customer'):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view