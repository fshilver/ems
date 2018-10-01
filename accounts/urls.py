from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import (
    UserListByGroupView,
    UserSignUpView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)
from .views import GroupListView, GroupCreateView, GroupDeleteView, GroupUpdateView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users_by_group/', UserListByGroupView.as_view(), name='users_by_group'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
    path('groups/update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
]