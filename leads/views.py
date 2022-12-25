from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm
# Create your views here.

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads,
    }
    
    return render(request, "leads/lead_list.html", context)

def lead_detail(request, pk):
    print(pk)
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

# lead form with django Modelform

def  lead_create(request):
    
    form = LeadModelForm()

    if request.method == "POST":
        print("Reciving a post request")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            print("The new lead has been created")
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)


# def  lead_create(request):
    
#     form = LeadForm()

#     if request.method == "POST":
#         print("Reciving a post request")
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             agent = Agent.objects.first()

#             Lead.objects.create(
#                first_name=first_name,
#                last_name=last_name,
#                age=age,
#                agent=agent 
#             )
            
#             print("The new lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)