from django.shortcuts import render
from django.http import HttpResponse
from .models import Lead
# Create your views here.

def home_page(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    # return HttpResponse("Hello world")
    # return render(request, "leads/home_page.html")
    return render(request, "second_page.html", context)