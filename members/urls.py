from django.urls import path
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('welcome/', RedirectView.as_view(pattern_name='welcome', permanent=False), name='welcome_legacy'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('club_treasury/', views.club_treasury, name='club_treasury'),
    path('gallery/', views.gallery, name='gallery'),
    path('club_events/', views.club_events, name='club_events'), 
    path('balance_graph/', views.balance_graph, name='balance_graph'), 
    path('contact/', views.contact, name='contact'),    
] 
