from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from itertools import chain


class UserListByGroup(ListView):

    template_name = "accounts/group_user_list.html"
    context_object_name = 'allUsers'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        groups = []
        for group in Group.objects.filter(user=self.request.user):
            group_dict = {}
            group_dict['name'] = group.name
            group_dict['users'] = User.objects.filter(groups__name__exact=group.name)
            groups.append(group_dict)

        context['groups'] = groups
        return context