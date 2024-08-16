# Import necessary modules
from django.contrib import admin # Django admin module
from django.urls import path	 # URL routing
from django.conf import settings # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # Static files serving
from . import views

# Define URL patterns
urlpatterns = [
    
	path('', views.login_page, name='login_page'), # Login page
	path('register/', views.register_page, name='register'), # Registration page
    path("admin/", admin.site.urls), # Admin interface
]


