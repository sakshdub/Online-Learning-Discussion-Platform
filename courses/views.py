from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, CourseMaterial
from .forms import CourseForm, CourseMaterialForm, ContactForm
from django.views.generic import ListView

# Homepage View
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

# Dedicated "All Courses" Page View
def all_courses_view(request):
    courses = Course.objects.all()
    return render(request, 'courses/all_courses.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    enrolled = False
    if request.user.is_authenticated and request.user.role == 'student':
        enrolled = course.students.filter(id=request.user.id).exists()
    materials = course.materials.all()
    return render(request, 'courses/course_detail.html', {
        'course': course,
        'enrolled': enrolled,
        'materials': materials
    })

@login_required
def add_course(request):
    if request.user.role != 'instructor':
        messages.warning(request, "Only instructors can add new courses.")
        return redirect('home')
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            messages.success(request, "Course created successfully!")
            return redirect('home')
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

@login_required
def enroll_in_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.user.role == 'student':
        if not course.students.filter(id=request.user.id).exists():
            course.students.add(request.user)
            messages.success(request, f"You have successfully enrolled in {course.title}.")
        else:
            messages.info(request, "You are already enrolled in this course.")
    return redirect('course_detail', pk=course.pk)

@login_required
def add_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user != course.instructor:
        messages.warning(request, "You are not authorized.")
        return redirect('course_detail', pk=course.id)
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, "Material uploaded successfully!")
            return redirect('course_detail', pk=course.id)
    else:
        form = CourseMaterialForm()
    return render(request, 'courses/course_form.html', {'form': form, 'course': course})

# Static Page Views
def about_view(request):
    return render(request, 'pages/about.html')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for your message! We'll get back to you soon.")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})

def discussion_view(request):
    if request.method == 'POST':
        messages.info(request, "The main discussion forum is under construction. Please use the course-specific forums.")
        return redirect('discussion')
    return render(request, 'pages/discussion.html')