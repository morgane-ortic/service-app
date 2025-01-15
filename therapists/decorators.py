from django.shortcuts import redirect

def therapist_required(view_func):
    '''if user is not logged in as a therapist, redirect to homepage'''
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'therapist'):
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view