from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('add/', views.add_course, name='add_course'),
    path('<int:pk>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('<int:course_id>/add_material/', views.add_material, name='add_material'),
]