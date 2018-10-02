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
    EquipmentSpecDetailView,
    UsableEquipmentListView,
    UsedEquipmentListView,
    ApplyToUseEquipmentView,
    ApplyEquipmentListView,
    ApplyEquipmentAcceptView,
    ApplyEquipmentRejectView,
    ReturnEquipmentView,
    ReturnEquipmentListView,
    ReturnEquipmentAcceptView,
    ReturnEquipmentRejectView,
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
    path('eq/usable/', UsableEquipmentListView.as_view(), name='usable_eq_list'),
    path('eq/used/', UsedEquipmentListView.as_view(), name='used_eq_list'),
    path('eq/apply/', ApplyEquipmentListView.as_view(), name='apply_eq_list'),
    path('eq/apply/<int:pk>/', ApplyToUseEquipmentView.as_view(), name='apply_eq'),
    path('eq/apply/<int:pk>/accept/', ApplyEquipmentAcceptView.as_view(), name='apply_eq_accept'),
    path('eq/apply/<int:pk>/reject/', ApplyEquipmentRejectView.as_view(), name='apply_eq_reject'),
    path('eq/return/', ReturnEquipmentListView.as_view(), name='return_eq_list'),
    path('eq/return/<int:pk>/', ReturnEquipmentView.as_view(), name='return_eq'),
    path('eq/return/<int:pk>/accept/', ReturnEquipmentAcceptView.as_view(), name='return_eq_accept'),
    path('eq/return/<int:pk>/reject/', ReturnEquipmentRejectView.as_view(), name='return_eq_reject'),
    path('eq/create/', EquipmentCreateView.as_view(), name='eq_create'),
    path('eq/update/<int:pk>', EquipmentUpdateView.as_view(), name='eq_update'),
    path('eq/delete/<int:pk>', EquipmentDeleteView.as_view(), name='eq_delete'),
    path('eq_spec/update/<int:pk>/', EquipmentSpecUpdateView.as_view(), name='eq_spec_update'),
    path('eq_spec/<int:pk>/', EquipmentSpecDetailView.as_view(), name='eq_spec_detail'),
]