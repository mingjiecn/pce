from django.urls import path
from about import views

urlpatterns = [
    path('about', views.about, name='about'),
    path('more', views.more, name='more'),
    path('team', views.team, name='team'),
]