from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^welcome/?$', views.welcome, name='welcome'),
    re_path(r'^members/?$', views.members, name='members'),
    re_path(r'^members/details/(?P<id>\d+)/?$', views.details, name='details'),
    re_path(r'^testing/?$', views.testing, name='testing'),
    re_path(r'^club_treasury/?$', views.club_treasury, name='club_treasury'),
    re_path(r'^gallery/?$', views.gallery, name='gallery'),
    re_path(r'^club_events/?$', views.club_events, name='club_events'), 
    re_path(r'^balance_graph/?$', views.balance_graph, name='balance_graph'), 
    re_path(r'^contact/?$', views.contact, name='contact'),  
]
