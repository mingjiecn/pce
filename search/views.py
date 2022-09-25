from django.shortcuts import render
from search.models import Patient, Pathology_TR
from django.core import serializers
from django.http import JsonResponse
from search.filters import Pathology_TR_Filter, PatientFilter
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

#import plotly.graph_objs as go
#from plotly.offline import plot

from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import TemplateView
import json 

def search(request):
    return render(request, 'search.html', {})

def dashboard(request):
    return render(request, 'dashboard.html', {})

def pivot_data(request):
    dataset = Patient.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

def patient_list(request):

    f = PatientFilter(request.GET, queryset=Patient.objects.all())
    patients = f.qs
    p = Paginator(patients, 20) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    #add radiation to patient list
    for patient in page_obj:
        for field in patient._meta.fields:
            print(field)
        break

        #patient.radiation = patient.radiation_set.all()

    context = {
        'page_obj': page_obj,
        'filter': f,
                
    }


    return render(request, 'search/patient_list.html', context)

def patholoy_tr_list(request):

    f = Pathology_TR_Filter(request.GET, queryset=Pathology_TR.objects.all())
    pathology_TRs = f.qs
    p = Paginator(pathology_TRs, 20) 
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    context = {
        'page_obj': page_obj,
        'filter': f,
                
    }

    return render(request, 'search/pathology_rt_list.html', context)