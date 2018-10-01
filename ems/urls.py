from django.urls import path
from .views import (
    RepairStatusListView,
    RepairStatusCreateView,
    RepairStatusUpdateView,
    RepairStatusDeleteView,
    EquipmentTypeListView,
    EquipmentTypeCreateView,
    EquipmentTypeUpdateView,
    EquipmentTypeDeleteView,
    EquipmentListView,
    EquipmentCreateView,
    EquipmentUpdateView,
    EquipmentDeleteView,
    EquipmentSpecUpdateView,
)

urlpatterns = [
    path('repair_status/', RepairStatusListView.as_view(), name='repair_status_list'),
    path('repair_status/create/', RepairStatusCreateView.as_view(), name='repair_status_create'),
    path('repair_status/update/<int:pk>', RepairStatusUpdateView.as_view(), name='repair_status_update'),
    path('repair_status/delete/<int:pk>', RepairStatusDeleteView.as_view(), name='repair_status_delete'),
    path('eq_type/', EquipmentTypeListView.as_view(), name='eq_type_list'),
    path('eq_type/create/', EquipmentTypeCreateView.as_view(), name='eq_type_create'),
    path('eq_type/update/<int:pk>', EquipmentTypeUpdateView.as_view(), name='eq_type_update'),
    path('eq_type/delete/<int:pk>', EquipmentTypeDeleteView.as_view(), name='eq_type_delete'),
    path('eq/', EquipmentListView.as_view(), name='eq_list'),
    path('eq/create/', EquipmentCreateView.as_view(), name='eq_create'),
    path('eq/update/<int:pk>', EquipmentUpdateView.as_view(), name='eq_update'),
    path('eq/delete/<int:pk>', EquipmentDeleteView.as_view(), name='eq_delete'),
    path('eq_spec/update/<int:pk>/', EquipmentSpecUpdateView.as_view(), name='eq_spec_update'),
]