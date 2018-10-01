from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from .forms import SigninForm


class UserListByGroupView(ListView):

    template_name = "accounts/user_by_group_list.html"
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
            group_dict['users'] = User.objects.filter(groups__name__exact=group.name).exclude(id=self.request.user.id)
            groups.append(group_dict)

        context['groups'] = groups
        return context


class UserListView(ListView):
    model = get_user_model()
    template_name = "accounts/user_list.html"


class UserSignUpView(CreateView):
    '''
    팀 관리자(is_staff=True) 가 사용하는 user create view
    '''
    model = get_user_model()
    form_class = SigninForm
    template_name = "accounts/user_form.html"
    success_url = reverse_lazy('accounts:users_by_group')

    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs['user'] = self.request.user
        return form_kwargs


class UserCreateView(CreateView):
    '''
    superuser 가 사용하는 user create view
    '''
    model = get_user_model()
    form_class = SigninForm
    template_name = "accounts/user_create.html"
    success_url = reverse_lazy('accounts:user_list')


class UserUpdateView(UpdateView):
    '''
    superuser 가 사용하는 user update view
    '''
    model = get_user_model()
    form_class = SigninForm
    template_name = "accounts/user_create.html"
    success_url = reverse_lazy('accounts:user_list')


class UserDeleteView(DeleteView):
    '''
    superuser 가 사용하는 user delete view
    '''
    model = get_user_model()
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy('accounts:user_list')


class GroupListView(ListView):
    model = Group
    template_name = "accounts/group_list.html"


class GroupCreateView(CreateView):
    model = Group
    template_name = "accounts/group_form.html"
    success_url = reverse_lazy('accounts:group_list')
    fields = ('name',)

    def get_context_data(self, **kwargs):
        cx = super().get_context_data(**kwargs)
        print(cx)
        return cx


class GroupDeleteView(DeleteView):
    model = Group
    template_name = "accounts/group_delete.html"
    success_url = reverse_lazy('accounts:group_list')


class GroupUpdateView(UpdateView):
    model = Group
    fields = ('name',)
    template_name = "accounts/group_form.html"
    success_url = reverse_lazy('accounts:group_list')