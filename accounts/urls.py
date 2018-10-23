from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import (
    UserListByGroupView,
    UserSignUpView,
    UserListView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
    CustomLoginView,
    PasswordChangeView,
)
from .ajax_views import (
    activate_users,
    deactivate_users,
    delete_groups,
)

from .views import GroupListView, GroupCreateView, GroupDeleteView, GroupUpdateView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/activate/', activate_users, name='activate_users'),
    path('users/deactivate/', deactivate_users, name='deactivate_users'),
    path('users/create/', UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('users_by_group/', UserListByGroupView.as_view(), name='users_by_group'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('groups/', GroupListView.as_view(), name='group_list'),
    path('groups/create/', GroupCreateView.as_view(), name='group_create'),
    path('groups/delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
    path('groups/update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('groups/delete/ajax/', delete_groups, name='delete_group_ajax'),
]
