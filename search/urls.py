from django.urls import path
from search import views


urlpatterns = [
    path('search', views.search, name='search'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('data', views.pivot_data, name='pivot_data'),
    path('', views.patient_list, name='patients'),
    path('pathology_tr', views.patholoy_tr_list, name='pathology_tr'),
    
]