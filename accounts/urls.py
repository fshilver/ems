from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import UserListByGroupView, UserSignUpView

urlpatterns = [
    path('groups/', UserListByGroupView.as_view(), name='users_by_group'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
]