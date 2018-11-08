from django.contrib import admin

from .models import (
    RepairStatus,
    EquipmentType,
    Equipment,
    EquipmentSpec,
    EquipmentHistory,
    EquipmentRepairHistory,
)

admin.site.register(RepairStatus)
admin.site.register(EquipmentType)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'management_number', 'kind', 'serial_number', 'current_user', 'status')


@admin.register(EquipmentSpec)
class EquipmentSpecAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipment', 'cpu', 'mem', 'change_date', 'change_user', 'reference', 'cost')


@admin.register(EquipmentHistory)
class EquipmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'check_out_date', 'user', 'purpose', 'check_in_duedate', 'manager_confirm', 'check_in_confirm', 'note', 'count')


@admin.register(EquipmentRepairHistory)
class EquipmentRepairHistoryAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'date', 'reason', 'result', 'cost', 'manager', 'reference', 'count')