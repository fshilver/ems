from django.contrib import admin

from .models import (
    RepairStatus,
    EquipmentType,
    Equipment,
    EquipmentSpec,
)

admin.site.register(RepairStatus)
admin.site.register(EquipmentType)
admin.site.register(EquipmentSpec)

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'current_user', 'status')