from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('student_rentals')
    else:
        return auth_views.LoginView.as_view(template_name='login.html')(request, *args, **kwargs)
