from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent, UserProfile
from django.shortcuts import reverse
from .forms import AgentModelForm


class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"
    
    def get_queryset(self):
        return Agent.objects.all()


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent-list")
    
    def form_valid(self, form):
        agent = form.save(commit=False)
        user = self.request.user
        if hasattr(user, 'userprofile'):
            agent.organisation = user.userprofile
        else:
            user_profile = UserProfile.objects.create(user=user)
            agent.organisation = user_profile
        agent.save()
        return super(AgentCreateView, self).form_valid(form)