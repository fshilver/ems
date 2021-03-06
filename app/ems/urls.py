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
    EquipmentApplyFormListView,
    EquipmentReturnFormListView,
    UsableEquipmentListView,
    UsedEquipmentListView,
    ApplyEquipmentListView,
    ReturnEquipmentListView,
    EquipmentHistoryListView,
    apply_eq_form_view,
    reject_eq_form_view,
    reject_return_eq_form_view,
    return_eq_form_view,
    checkin_eq_form_view,
    checkout_eq_form_view,
)

from .ajax_views import (
    accept_use_eq,
    reject_use_eq,
    accept_return_eq,
    delete_repair_status,
    delete_equipment_type,
    change_status_eq,
    cancel_apply_eq,
    cancel_return_eq,
)

urlpatterns = [
    path('repair_status/', RepairStatusListView.as_view(), name='repair_status_list'),
    path('repair_status/create/', RepairStatusCreateView.as_view(), name='repair_status_create'),
    path('repair_status/update/<int:pk>', RepairStatusUpdateView.as_view(), name='repair_status_update'),
    path('repair_status/delete/<int:pk>', RepairStatusDeleteView.as_view(), name='repair_status_delete'),

    path('repair_status/delete/ajax/', delete_repair_status, name='delete_repair_status_ajax'),

    path('eq_type/', EquipmentTypeListView.as_view(), name='eq_type_list'),
    path('eq_type/create/', EquipmentTypeCreateView.as_view(), name='eq_type_create'),
    path('eq_type/update/<int:pk>', EquipmentTypeUpdateView.as_view(), name='eq_type_update'),
    path('eq_type/delete/<int:pk>', EquipmentTypeDeleteView.as_view(), name='eq_type_delete'),

    path('eq_type/delete/ajax/', delete_equipment_type, name='delete_eq_type_ajax'),

    path('eq/usable/', UsableEquipmentListView.as_view(), name='usable_eq_list'), # 사용 신청 가능한 장비 목록
    path('eq/used/', UsedEquipmentListView.as_view(), name='used_eq_list'), # 사용 중인 장비 목록
    path('eq/apply/history/', EquipmentApplyFormListView.as_view(), name='apply_eq_history'), # 사용 신청 이력
    path('eq/return/history/', EquipmentReturnFormListView.as_view(), name='return_eq_history'), # 반납 신청 이력
    path('eq/apply/', ApplyEquipmentListView.as_view(), name='apply_eq_list'), # 사용 신청한 장비 목록
    path('eq/apply/ajax/', apply_eq_form_view, name='apply_eq_ajax'), # 장비 사용 신청
    path('eq/apply/accept/ajax/', accept_use_eq, name='apply_eq_accept_ajax'), # 장비 사용 승인
    path('eq/apply/reject/ajax/', reject_use_eq, name='apply_eq_reject_ajax'), # 장비 사용 거절
    path('eq/apply/reject/', reject_eq_form_view, name='reject_eq'), # 장비 사용 거절

    path('eq/apply/cancel/ajax/', cancel_apply_eq, name='cancel_apply_eq_ajax'), # 장비 사용 신청 취소
    path('eq/return/cancel/ajax/', cancel_return_eq, name='cancel_return_eq_ajax'), # 장비 반납 신청 취소
    path('eq/return/', ReturnEquipmentListView.as_view(), name='return_eq_list'), # 장비 반납 신청 목록
    path('eq/return/ajax/', return_eq_form_view, name='return_eq'), # 장비 반납 신청
    path('eq/return/accept/ajax/', accept_return_eq, name='accept_return_eq_ajax'), # 장비 반납 승인
    path('eq/return/reject/ajax/', reject_return_eq_form_view, name='reject_return_eq'), # 장비 반납 거절
    path('eq/checkin/', checkin_eq_form_view, name='checkin_eq'), # 관리자용 장비 반납 view
    path('eq/checkout/', checkout_eq_form_view, name='checkout_eq'), # 관리자용 장비 반출 view

    # 장비 CRUD
    path('eq/', EquipmentListView.as_view(), name='eq_list'),
    path('eq/create/', EquipmentCreateView.as_view(), name='eq_create'),
    path('eq/update/<int:pk>', EquipmentUpdateView.as_view(), name='eq_update'),
    path('eq/delete/<int:pk>', EquipmentDeleteView.as_view(), name='eq_delete'),

    # 장비 상태 변경
    path('eq/change_status/', change_status_eq, name='change_status_eq_ajax'),

    path('eq_spec/update/<int:pk>/', EquipmentSpecUpdateView.as_view(), name='eq_spec_update'),
    path('eq_spec/<int:pk>/', EquipmentSpecDetailView.as_view(), name='eq_spec_detail'),

    # 장비 대여/반납 이력
    path('eq_history/<int:eq_id>/', EquipmentHistoryListView.as_view(), name='eq_history_list'),
]