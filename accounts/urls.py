from django.urls import include, path
from django.contrib.auth import views as auth_views
from .views import UserListByGroup

urlpatterns = [
    path('groups/', UserListByGroup.as_view(), name='users_by_group'),
]