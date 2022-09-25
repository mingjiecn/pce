from django.urls import path
from search import views


urlpatterns = [
    path('', views.search, name='search'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('data', views.pivot_data, name='pivot_data'),
    path('patients', views.patient_list),
    path('pathology_tr', views.patholoy_tr_list),
    
]