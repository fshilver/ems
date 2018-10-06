from django.http import JsonResponse
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
    paginate_by = 10


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


class UsableEquipmentListView(ListView):
    model = Equipment
    queryset = Equipment.objects.filter(status=Equipment.USABLE)
    template_name = 'ems/usable_eq_list.html'
    paginate_by = 10


class UsedEquipmentListView(ListView):
    model = Equipment
    template_name = 'ems/used_eq_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Equipment.objects.filter(status=Equipment.USED).filter(current_user=self.request.user)
        return queryset


class ApplyEquipmentListView(ListView):
    '''
    사용 신청한 장비 목록
    '''
    model = Equipment
    queryset = Equipment.objects.filter(status=Equipment.WAITING_FOR_ACCEPT_TO_USE)
    template_name = 'ems/apply_eq_list.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Equipment.objects.filter(status=Equipment.WAITING_FOR_ACCEPT_TO_USE)
        else:
            return Equipment.objects.filter(status=Equipment.WAITING_FOR_ACCEPT_TO_USE).filter(current_user=self.request.user)


class ApplyToUseEquipmentView(UpdateView):
    '''
    장비 사용 신청
    '''
    model = Equipment
    fields = ('status',)
    template_name = 'ems/apply_eq_form.html'
    success_url = reverse_lazy('ems:usable_eq_list')

    def form_valid(self, form):
        form.instance.current_user = self.request.user
        form.instance.status = Equipment.WAITING_FOR_ACCEPT_TO_USE
        return super().form_valid(form)


class ApplyEquipmentAcceptView(UpdateView):
    '''
    장비 사용 신청 승인
    '''
    model = Equipment
    fields = ('status',)
    template_name = 'ems/apply_eq_accept_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USED
        return super().form_valid(form)


class ApplyEquipmentRejectView(UpdateView):
    '''
    장비 사용 신청 취소
    '''
    model = Equipment
    fields = ('status',)
    template_name = 'ems/apply_eq_reject_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USABLE
        form.instance.current_user = None
        return super().form_valid(form)


class ReturnEquipmentListView(ListView):
    '''
    반납 신청한 장비 목록
    '''
    model = Equipment
    queryset = Equipment.objects.filter(status=Equipment.WAITING_FOR_ACCEPT_TO_RETURN)
    template_name = 'ems/return_eq_list.html'
    paginate_by = 10


class ReturnEquipmentView(UpdateView):
    '''
    장비 반납 신청
    '''
    model = Equipment
    fields = ('status',)
    template_name = 'ems/return_eq.html'
    success_url = reverse_lazy('ems:used_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.WAITING_FOR_ACCEPT_TO_RETURN
        return super().form_valid(form)


class ReturnEquipmentAcceptView(UpdateView):
    '''
    장비 반납 신청 승인
    '''
    model = Equipment
    fields = ('status',)
    template_name = 'ems/return_eq_accept_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USABLE
        form.instance.current_user = None
        return super().form_valid(form)


class ReturnEquipmentRejectView(UpdateView):
    '''
    장비 반납 신청 취소
    '''
    model = Equipment
    fields = ('status',)
    template_name = 'ems/return_eq_reject_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USED
        return super().form_valid(form)


####################################
# EquipmentSpec
####################################
class EquipmentSpecUpdateView(UpdateView):
    model = EquipmentSpec
    form_class = EquipmentSpecForm
    template_name = 'ems/eq_spec_form.html'
    success_url = reverse_lazy('ems:eq_list')

    def get_object(self):
        pk = self.kwargs.get('pk')
        eq = Equipment.objects.get(pk=pk)
        return EquipmentSpec.objects.filter(equipment__exact=eq).order_by('-count').first()


class EquipmentSpecDetailView(DetailView):
    model = EquipmentSpec
    template_name = 'ems/eq_spec_detail.html'

    def render_to_response(self, context):
        if self.request.is_ajax():
            return  JsonResponse({
                'cpu': self.object.cpu,
                'mem': self.object.mem,
                'hdd': self.object.hdd,
                'nic': self.object.nic,
                'graphic': self.object.graphic,
                'etc': self.object.etc,
                'text': self.object.text,
            })

        # template rendering
        return super().render_to_response(context)

    def get_object(self):
        pk = self.kwargs.get('pk')
        eq = Equipment.objects.get(pk=pk)
        return EquipmentSpec.objects.filter(equipment__exact=eq).order_by('-count').first()

