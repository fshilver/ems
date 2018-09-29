from django.contrib import admin

from .models import (
    RepairStatus,
    EquipmentType,
)

admin.site.register(RepairStatus)
admin.site.register(EquipmentType)