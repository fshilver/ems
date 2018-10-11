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

from .ajax_views import (
    apply_use_eq,
    accept_use_eq,
    reject_use_eq,
    apply_return_eq,
    accept_return_eq,
    reject_return_eq,
    delete_repair_status,
)

urlpatterns = [
    path('repair_status/', RepairStatusListView.as_view(), name='repair_status_list'),
    path('repair_status/create/', RepairStatusCreateView.as_view(), name='repair_status_create'),
    path('repair_status/update/<int:pk>', RepairStatusUpdateView.as_view(), name='repair_status_update'),
    path('repair_status/delete/<int:pk>', RepairStatusDeleteView.as_view(), name='repair_status_delete'),

    path('repair_status/delete/ajax/>', delete_repair_status, name='delete_repair_status_ajax'),


    path('eq_type/', EquipmentTypeListView.as_view(), name='eq_type_list'),
    path('eq_type/create/', EquipmentTypeCreateView.as_view(), name='eq_type_create'),
    path('eq_type/update/<int:pk>', EquipmentTypeUpdateView.as_view(), name='eq_type_update'),
    path('eq_type/delete/<int:pk>', EquipmentTypeDeleteView.as_view(), name='eq_type_delete'),

    path('eq/', EquipmentListView.as_view(), name='eq_list'),
    path('eq/usable/', UsableEquipmentListView.as_view(), name='usable_eq_list'),

    # 사용 중인 장비 목록
    path('eq/used/', UsedEquipmentListView.as_view(), name='used_eq_list'),

    path('eq/apply/', ApplyEquipmentListView.as_view(), name='apply_eq_list'),

    # 장비 사용 신청
    path('eq/apply/ajax/', apply_use_eq, name='apply_eq_ajax'),
    path('eq/apply/<int:pk>/', ApplyToUseEquipmentView.as_view(), name='apply_eq'),

    # 장비 사용 승인
    path('eq/apply/accept/ajax/', accept_use_eq, name='apply_eq_accept_ajax'),
    path('eq/apply/<int:pk>/accept/', ApplyEquipmentAcceptView.as_view(), name='apply_eq_accept'),

    # 장비 사용 거절
    path('eq/apply/reject/ajax/', reject_use_eq, name='apply_eq_reject_ajax'),
    path('eq/apply/<int:pk>/reject/', ApplyEquipmentRejectView.as_view(), name='apply_eq_reject'),

    # 장비 반납 신청 목록
    path('eq/return/', ReturnEquipmentListView.as_view(), name='return_eq_list'),

    # 장비 반납 신청
    path('eq/return/ajax/', apply_return_eq, name='apply_return_eq_ajax'),
    path('eq/return/<int:pk>/', ReturnEquipmentView.as_view(), name='return_eq'),

    # 장비 반납 승인
    path('eq/return/accept/ajax/', accept_return_eq, name='accept_return_eq_ajax'),
    path('eq/return/<int:pk>/accept/', ReturnEquipmentAcceptView.as_view(), name='return_eq_accept'),

    # 장비 반납 거절
    path('eq/return/reject/ajax/', reject_return_eq, name='reject_return_eq_ajax'),
    path('eq/return/<int:pk>/reject/', ReturnEquipmentRejectView.as_view(), name='return_eq_reject'),

    path('eq/create/', EquipmentCreateView.as_view(), name='eq_create'),
    path('eq/update/<int:pk>', EquipmentUpdateView.as_view(), name='eq_update'),
    path('eq/delete/<int:pk>', EquipmentDeleteView.as_view(), name='eq_delete'),

    path('eq_spec/update/<int:pk>/', EquipmentSpecUpdateView.as_view(), name='eq_spec_update'),
    path('eq_spec/<int:pk>/', EquipmentSpecDetailView.as_view(), name='eq_spec_detail'),
]