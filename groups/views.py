from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.urls import reverse
from django.views import generic
from django.db import IntegrityError

from groups.models import Group,GroupMember

# Create your views here.

class CreateGroup(generic.CreateView,LoginRequiredMixin):
    fields = ('name','desccription')
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,'Warning already a member!')
        else:
            messages.success(self.request,'You are now a member')

        return super().get(request,*args,**kwargs)