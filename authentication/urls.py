# Import necessary modules
from django.contrib import admin # Django admin module
from django.urls import path	 # URL routing
#from authentication.views import * # Import views from the authentication app
from django.conf import settings # Application settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # Static files serving
from . import views

# Define URL patterns
urlpatterns = [
	#path('', views.home, name="recipes"),	 # Home page
	path("admin/", admin.site.urls),		 # Admin interface
	path('', views.login_page, name='login_page'), # Login page
	path('register/', views.register_page, name='register'), # Registration page
]

# Serve media files if DEBUG is True (development mode)
#if settings.DEBUG:
#	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files using staticfiles_urlpatterns
#urlpatterns += staticfiles_urlpatterns()
