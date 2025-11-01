from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'instructor'})
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_courses', blank=True)
    def __str__(self):
        return self.title

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='course_materials/') 
    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message from {self.name}"