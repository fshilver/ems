from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.conf import settings
from .forms import (
    SignUpForm,
    LoginForm,
    CustomUserChangeForm,
    UserUpdateForm,
)


class CustomLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'



class UserListView(ListView):
    model = get_user_model()
    template_name = "accounts/user_list.html"

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                user = {
                    'id': obj.id,
                    'email': obj.email,
                    'name': obj.name,
                    'is_active': obj.is_active,
                    'is_staff': obj.is_staff,
                }
                data.append(user)

            return JsonResponse({"data": data})
        return super().render_to_response(context)



class UserCreateView(CreateView):
    '''
    superuser 가 사용하는 user create view
    '''
    model = get_user_model()
    form_class = SignUpForm
    template_name = "accounts/user_create.html"
    success_url = reverse_lazy('accounts:user_list')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['accounts/user_modal_form.html']
        return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return HttpResponse("성공")
        return response



class UserUpdateView(UpdateView):
    """
    superuser 가 사용하는 user update view
    """
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = "accounts/user_create.html"
    success_url = reverse_lazy('accounts:user_list')

    def get_template_names(self):
        if self.request.is_ajax():
            return ['accounts/user_modal_form.html']
        return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return HttpResponse("성공")
        return response



class UserDeleteView(DeleteView):
    """
    superuser 가 사용하는 user delete view
    """
    model = get_user_model()
    template_name = "accounts/user_delete.html"
    success_url = reverse_lazy('accounts:user_list')



class PasswordChangeView(auth_views.PasswordChangeView):
    """
    사용자가 자신의 패스워드를 변경하는 modal view
    """
    template_name = "accounts/password_change_form.html"
    success_url = settings.LOGIN_REDIRECT_URL

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        for field in form.fields:
            form.fields[field].widget.attrs.update({'class': 'form-control'})
        return form