from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import RepairStatus, EquipmentType


####################################
# RepairStatus 
####################################
class RepairStatusListView(ListView):
    model = RepairStatus
    template_name = 'ems/repair_status_list.html'


class RepairStatusCreateView(CreateView):
    model = RepairStatus
    template_name = 'ems/repair_status_create.html'
    success_url = reverse_lazy('ems:repair_status_list')
    fields = ('label',)


class RepairStatusUpdateView(UpdateView):
    model = RepairStatus
    template_name = 'ems/repair_status_update.html'
    success_url = reverse_lazy('ems:repair_status_list')
    fields = ('label',)


class RepairStatusDeleteView(DeleteView):
    model = RepairStatus
    template_name = 'ems/repair_status_delete.html'
    success_url = reverse_lazy('ems:repair_status_list')


####################################
# EquipmentType
####################################
class EquipmentTypeListView(ListView):
    model = EquipmentType
    template_name = 'ems/eq_type_list.html'


class EquipmentTypeCreateView(CreateView):
    model = EquipmentType
    template_name = 'ems/eq_type_create.html'
    success_url = reverse_lazy('ems:eq_type_list')
    fields = ('label',)


class EquipmentTypeUpdateView(UpdateView):
    model = EquipmentType
    template_name = 'ems/eq_type_update.html'
    success_url = reverse_lazy('ems:eq_type_list')
    fields = ('label',)


class EquipmentTypeDeleteView(DeleteView):
    model = EquipmentType
    template_name = 'ems/eq_type_delete.html'
    success_url = reverse_lazy('ems:eq_type_list')
