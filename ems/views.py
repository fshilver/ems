from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from .models import (
    RepairStatus,
    EquipmentType,
    Equipment,
    EquipmentSpec,
)
from .forms import (
    EquipmentCreationForm,
    EquipmentSpecForm,
    EquipmentForm,
)


####################################
# RepairStatus 
####################################
class RepairStatusListView(ListView):
    model = RepairStatus
    template_name = 'ems/repair_status_list.html'


class RepairStatusCreateView(CreateView):
    model = RepairStatus
    template_name = 'ems/repair_status_form.html'
    success_url = reverse_lazy('ems:repair_status_list')
    fields = ('label',)


class RepairStatusUpdateView(UpdateView):
    model = RepairStatus
    template_name = 'ems/repair_status_form.html'
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
    template_name = 'ems/eq_type_form.html'
    success_url = reverse_lazy('ems:eq_type_list')
    fields = ('label',)


class EquipmentTypeUpdateView(UpdateView):
    model = EquipmentType
    template_name = 'ems/eq_type_form.html'
    success_url = reverse_lazy('ems:eq_type_list')
    fields = ('label',)


class EquipmentTypeDeleteView(DeleteView):
    model = EquipmentType
    template_name = 'ems/eq_type_delete.html'
    success_url = reverse_lazy('ems:eq_type_list')


####################################
# Equipment
####################################
class EquipmentListView(ListView):
    model = Equipment
    template_name = 'ems/eq_list.html'


class EquipmentCreateView(CreateView):
    model = Equipment
    form_class = EquipmentCreationForm
    template_name = 'ems/eq_form.html'
    success_url = reverse_lazy('ems:eq_list')


class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'ems/eq_form.html'
    success_url = reverse_lazy('ems:eq_list')


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'ems/eq_delete.html'
    success_url = reverse_lazy('ems:eq_list')


####################################
# EquipmentSpec
####################################
class EquipmentSpecUpdateView(UpdateView):
    model = EquipmentSpec
    form_class = EquipmentSpecForm
    template_name = 'ems/eq_spec_form.html'
    success_url = reverse_lazy('ems:eq_list')