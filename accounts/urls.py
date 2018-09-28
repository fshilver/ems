from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import UserListByGroupView, UserSignUpView
from .views import GroupListView, GroupCreateView, GroupDeleteView, GroupUpdateView

urlpatterns = [
    path('users/', UserListByGroupView.as_view(), name='users_by_group'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/delete/<int:pk>', GroupDeleteView.as_view(), name='group_delete'),
    path('groups/update/<int:pk>', GroupUpdateView.as_view(), name='group_update'),
]