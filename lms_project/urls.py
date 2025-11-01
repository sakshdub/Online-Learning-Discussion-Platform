from django.contrib import admin
from django.urls import path, include
from courses.views import (
    CourseListView,
    all_courses_view,
    about_view,
    contact_view,
    discussion_view
)
# Add these two imports for media files
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main Site Pages
    path('', CourseListView.as_view(), name='home'),
    path('courses/', all_courses_view, name='course_list_page'),
    path('about/', about_view, name='about'),
    path('contact/', contact_view, name='contact'),
    path('discussion/', discussion_view, name='discussion'),

    # App URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('course/', include('courses.urls')),
    path('forums/', include('forums.urls')),
]

# Add this block at the end to serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)