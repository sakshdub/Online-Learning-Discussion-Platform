from django.contrib import admin
from .models import Category, Course, CourseMaterial, ContactMessage

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(CourseMaterial)
admin.site.register(ContactMessage)