from django.shortcuts import render

from django.db.models.functions import Coalesce

# Create your views here.
def about(request):
    return render(request, 'about.html', {})

def more(request):
    
    context = {

    }
    return render(request, 'more.html', context)

def team(request):
    return render(request, 'team.html', {})