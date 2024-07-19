from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
    path('template2/', views.template2, name='template2'),
    path('member_fees_summary/', views.member_fees_summary, name='members_fees_summary'),
    path('gallery/', views.gallery, name='gallery'),
    path('club_events/', views.club_events, name='club_events'),
    
]