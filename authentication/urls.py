from django.urls import path
from . import views

urlpatterns = [
	path('login/', views.login_page, name='login_page'),
	path('register/', views.register_page, name='register'),
    # Compatibility with Django's default LOGIN_URL (/accounts/login/)
    path('accounts/login/', views.login_page, name='login'),
]


