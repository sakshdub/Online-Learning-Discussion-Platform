from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from courses.models import Course

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    
@login_required
def dashboard(request):
    user = request.user
    
    if user.role == 'student':
        enrolled_courses = user.enrolled_courses.all()
        context = {'courses': enrolled_courses}
        return render(request, 'users/student_dashboard.html', context)
        
    elif user.role == 'instructor':
        created_courses = Course.objects.filter(instructor=user)
        context = {'courses': created_courses}
        return render(request, 'users/instructor_dashboard.html', context)
    
    elif user.role == 'admin' or user.is_superuser:
        return redirect('admin:index')