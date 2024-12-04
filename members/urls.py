from django.urls import path
from . import views


urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    path('club_treasury/', views.club_treasury, name='club_treasury'),
    path('gallery/', views.gallery, name='gallery'),
    path('club_events/', views.club_events, name='club_events'), 
    path('balance_graph/', views.balance_graph, name='balance_graph'), 
    path('contact/', views.contact, name='contact'),    
] 
