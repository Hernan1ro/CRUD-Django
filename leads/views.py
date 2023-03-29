from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm
from django.views.generic import TemplateView, DeleteView, UpdateView, CreateView, ListView, DetailView
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
# Create your views here.

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")


class landingPageView(TemplateView):
    template_name = "landing.html"



def landing_page(request):
    return render(request, "landing.html")


class LeadListView(LoginRequiredMixin ,ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"
    
    # initial queryset of leads for the entire organisation
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation, agent__isnull=False)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        
        # filter 
        
        return queryset 
    def get_context_data(self, *kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(*kwargs)
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile, agent__isnull=True)
            context.update({
                "unassigned_leads": queryset
            })        
        return context

# def lead_list(request):
#     leads = Lead.objects.all()
#     context = {
#         "leads": leads,
#     }
    
#     return render(request, "leads/lead_list.html", context)

class LeadDetailView(LoginRequiredMixin ,DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"
    
    # initial queryset of leads for the entire organisation
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        
        # filter 
        
        return queryset 


# def lead_detail(request, pk):
#     lead = Lead.objects.get(id=pk)
#     context = {
#         "lead": lead
#     }
#     return render(request, "leads/lead_detail.html", context)

class LeadCreateView(OrganisorAndLoginRequiredMixin, CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    def form_valid(self, form):
        # TODO sen email
        send_mail(
            subject="A lead has been created", 
            message="Go to the site to see the lead", 
            from_email="test@test.com", 
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)


# def  lead_create(request):
    
#     form = LeadModelForm()

#     if request.method == "POST":
#         print("Reciving a post request")
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("The new lead has been created")
#             return redirect("/leads")
#     context = {
#         "form": form
#     }
#     return render(request, "leads/lead_create.html", context)

# lead update form with django Modelform

class LeadUpdateView(OrganisorAndLoginRequiredMixin, UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    
    # initial queryset of leads for the entire organisation
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            return Lead.objects.filter(organisation=user.userprofile)
        

    def get_success_url(self):
        return reverse("leads:lead-list")

# def lead_update(request, pk):
#     lead = Lead.objects.get(pk=pk)
#     form = LeadModelForm(instance=lead)

#     if request.method == "POST":
#         form = LeadModelForm(request.POST ,instance=lead)
#         if form.is_valid():
#             form.save()
#             return redirect("/leads")
#     context = {
#         "form" : form ,
#         "lead" : lead
#     }
#     return render(request, "leads/lead_update.html", context)

class LeadDeleteView(OrganisorAndLoginRequiredMixin, DeleteView):
    template_name = "leads/lead_delete.html"
    
    def get_success_url(self):
        return reverse("leads:lead-list")

    # initial queryset of leads for the entire organisation
    def get_queryset(self):
        user = self.request.user
        
        if user.is_organisor:
            return Lead.objects.filter(organisation=user.userprofile)


# def lead_delete(request, pk):
#     lead = Lead.objects.get(id=pk)
#     lead.delete()
#     return redirect("/leads")

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm
    
    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)
    
class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"