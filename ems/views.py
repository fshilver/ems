from django.db import transaction
from django.forms.models import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from .models import (
    RepairStatus,
    EquipmentType,
    Equipment,
    EquipmentSpec,
    EquipmentHistory,
    EquipmentApply,
)
from .forms import (
    EquipmentSpecForm,
    EquipmentForm,
    EquipmentUpdateForm,
    EquipmentApplyForm,
)
import re


####################################
# RepairStatus 
####################################
class RepairStatusListView(ListView):
    model = RepairStatus
    template_name = 'ems/repair_status_list.html'

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                status = {
                    "id": obj.id,
                    "label": obj.label
                }
                data.append(status)
            return JsonResponse({"data": data})
        
        return super().render_to_response(context)


class RepairStatusCreateView(CreateView):
    model = RepairStatus
    template_name = 'ems/repair_status_form.html'
    success_url = reverse_lazy('ems:repair_status_list')
    fields = ('label',)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['ems/repair_status_modal_form.html']
        return super().get_template_names()


class RepairStatusUpdateView(UpdateView):
    model = RepairStatus
    template_name = 'ems/repair_status_form.html'
    success_url = reverse_lazy('ems:repair_status_list')
    fields = ('label',)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['ems/repair_status_modal_form.html']
        return super().get_template_names()


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

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                status = {
                    "id": obj.id,
                    "label": obj.label
                }
                data.append(status)
            return JsonResponse({"data": data})
        
        return super().render_to_response(context)


class EquipmentTypeCreateView(CreateView):
    model = EquipmentType
    template_name = 'ems/eq_type_form.html'
    success_url = reverse_lazy('ems:eq_type_list')
    fields = ('label',)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['ems/eq_type_modal_form.html']
        return super().get_template_names()


class EquipmentTypeUpdateView(UpdateView):
    model = EquipmentType
    template_name = 'ems/eq_type_form.html'
    success_url = reverse_lazy('ems:eq_type_list')
    fields = ('label',)

    def get_template_names(self):
        if self.request.is_ajax():
            return ['ems/eq_type_modal_form.html']
        return super().get_template_names()


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = Equipment.STATUS
        return context

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                if obj.current_user is None:
                    current_user_name = '-'
                else:
                    current_user_name = obj.current_user.name

                if obj.purchase_request_user is None:
                    purchase_requester_name = '-'
                else:
                    purchase_requester_name = obj.purchase_request_user.name

                eq = {
                    'id': obj.id,
                    'management_number': obj.management_number,
                    'kind': obj.kind.label,
                    'model': obj.model,
                    'serial_number': obj.serial_number,
                    'purchase_date': obj.purchase_date,
                    'current_user': current_user_name,
                    'purchase_requester': purchase_requester_name,
                    'price': obj.price,
                    'status': obj.get_status_display(),
                }
                data.append(eq)
            return JsonResponse({"data":data})
        return super().render_to_response(context)


class EquipmentCreateView(CreateView):
    model = Equipment
    # form_class = EquipmentCreationForm
    form_class = EquipmentForm
    template_name = 'ems/eq_form.html'
    success_url = reverse_lazy('ems:eq_list')

    def get_template_names(self):
        if self.request.is_ajax():
            return 'ems/eq_modal_form.html'
        return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return HttpResponse("성공")
        return response


class EquipmentUpdateView(UpdateView):
    model = Equipment
    form_class = EquipmentUpdateForm
    template_name = 'ems/eq_form.html'
    success_url = reverse_lazy('ems:eq_list')

    def get_template_names(self):
        if self.request.is_ajax():
            return 'ems/eq_modal_form.html'
        return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return HttpResponse("성공")
        return response


class EquipmentDeleteView(DeleteView):
    model = Equipment
    template_name = 'ems/eq_delete.html'
    success_url = reverse_lazy('ems:eq_list')


class UsableEquipmentListView(ListView):
    """
    사용 가능한 장비 목록
    """
    model = Equipment
    queryset = Equipment.objects.filter(status=Equipment.USABLE)
    template_name = 'ems/usable_eq_list.html'

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                eq_data = {
                    'id': obj.id,
                    'management_number': obj.management_number,
                    'kind': obj.kind.label,
                    'model': obj.model,
                    'serial_number': obj.serial_number,
                    'purchase_date': obj.purchase_date
                    }
                data.append(eq_data)
            return  JsonResponse({'data': data})

        # template rendering
        return super().render_to_response(context)


class UsedEquipmentListView(ListView):
    """
    사용 중인 장비 목록
    """
    model = Equipment
    template_name = 'ems/used_eq_list.html'

    def get_queryset(self):
        queryset = Equipment.objects.filter(status=Equipment.USED).filter(current_user=self.request.user)
        return queryset

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                eq_data = {
                    'id': obj.id,
                    'management_number': obj.management_number,
                    'kind': obj.kind.label,
                    'model': obj.model,
                    'serial_number': obj.serial_number,
                    'purchase_date': obj.purchase_date
                }
                data.append(eq_data)

            return JsonResponse({'data': data})

        return super().render_to_response(context)


class ApplyEquipmentListView(ListView):
    """
    사용 신청한 장비 목록
    """
    model = EquipmentApply
    template_name = 'ems/apply_eq_list.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return EquipmentApply.objects.filter(user=self.request.user).filter(status=EquipmentApply.APPLIED)
        return EquipmentApply.objects.filter(status=EquipmentApply.APPLIED)


    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['ems/apply_eq_list_for_superadmin.html']
        else:
            return super().get_template_names()


    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            if self.object_list:
                for obj in self.object_list:
                    eq_data = {
                        'id': obj.id,
                        'equipment_id': obj.equipment.id,
                        'management_number': obj.equipment.management_number,
                        'serial_number': obj.equipment.serial_number,
                        'model': obj.equipment.model,
                        'requester': obj.user.name,
                        'check_in_duedate': obj.check_in_duedate,
                        'purpose': obj.purpose,
                    }
                    data.append(eq_data)
            return JsonResponse({'data': data})

        return super().render_to_response(context)



def apply_eq_form_view(request):
    """
    장비 사용 신청 modal form
    """
    if request.method == "POST":
        form = EquipmentApplyForm(request.POST)

        if form.is_valid():
            raw_string = form.cleaned_data.get('equipment_list') # string : ['1549,1548,1547'] 
            eq_id_list = re.sub("[\[\]']", '', raw_string).split(',') # -> list : ['1549', '1548', '1547']

            for id in eq_id_list:
                with transaction.atomic():
                    eq = Equipment.objects.select_for_update().get(pk=id, status=Equipment.USABLE) # TODO: ORM 개선, 404 처리
                    eq.status = Equipment.WAITING_FOR_ACCEPT_TO_USE
                    eq.current_user = request.user
                    eq.save()
                    eq_apply_form = EquipmentApply(user=request.user
                                                ,equipment=eq
                                                ,purpose=form.cleaned_data['purpose']
                                                ,check_in_duedate=form.cleaned_data['check_in_duedate']
                                                ,note=form.cleaned_data['note']
                    )
                    eq_apply_form.save()
            return redirect('ems:usable_eq_list')
        else:
            return render(request, "modal_form.html", context={"form": form})
        
    else:
        # use initial value for hidden field(equipment_list) from get params : ?equipment_list=10,11
        # in this case, get param name and hidden field name is same(equipment_list)
        form = EquipmentApplyForm(initial=request.GET)
    return render(request, "modal_form.html", context={"form": form})



class ApplyEquipmentAcceptView(UpdateView):
    """
    장비 사용 승인
    """
    model = Equipment
    fields = ('status',)
    template_name = 'ems/apply_eq_accept_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USED
        return super().form_valid(form)


class ApplyEquipmentRejectView(UpdateView):
    """
    장비 사용 신청 취소
    """
    model = Equipment
    fields = ('status',)
    template_name = 'ems/apply_eq_reject_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USABLE
        form.instance.current_user = None
        return super().form_valid(form)


class ReturnEquipmentListView(ListView):
    """
    반납 신청한 장비 목록
    """
    model = Equipment
    template_name = 'ems/return_eq_list.html'

    def get_template_names(self):
        if self.request.user.is_superuser:
            return ['ems/return_eq_list_for_superadmin.html']
        return super().get_template_names()


    def get_queryset(self):
        if self.request.user.is_superuser:
            return Equipment.objects.filter(status=Equipment.WAITING_FOR_ACCEPT_TO_RETURN)
        else:
            return Equipment.objects.filter(status=Equipment.WAITING_FOR_ACCEPT_TO_RETURN).filter(current_user=self.request.user)


    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            for obj in self.object_list:
                eq_data = {
                    'id': obj.id,
                    'management_number': obj.management_number,
                    'kind': obj.kind.label,
                    'model': obj.model,
                    'requester': obj.current_user.name,
                    'serial_number': obj.serial_number,
                    'purchase_date': obj.purchase_date
                    }
                data.append(eq_data)
            print("ajax view")
            return  JsonResponse({'data': data})

        print("template view")
        return super().render_to_response(context)


class ReturnEquipmentView(UpdateView):
    """
    장비 반납 신청
    """
    model = Equipment
    fields = ('status',)
    template_name = 'ems/return_eq.html'
    success_url = reverse_lazy('ems:used_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.WAITING_FOR_ACCEPT_TO_RETURN
        return super().form_valid(form)


class ReturnEquipmentAcceptView(UpdateView):
    """
    장비 반납 신청 승인
    """
    model = Equipment
    fields = ('status',)
    template_name = 'ems/return_eq_accept_form.html'
    success_url = reverse_lazy('ems:apply_eq_list')

    def form_valid(self, form):
        form.instance.status = Equipment.USABLE
        form.instance.current_user = None
        return super().form_valid(form)


class ReturnEquipmentRejectView(UpdateView):
    """
    장비 반납 신청 취소
    """
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

    def get_template_names(self):
        if self.request.is_ajax():
            return ['ems/eq_spec_modal_form.html']
        return super().get_template_names()

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            return HttpResponse("성공")
        return response


class EquipmentSpecDetailView(DetailView):
    model = EquipmentSpec
    template_name = 'ems/eq_spec_modal_detail.html'

    def get_object(self):
        eq = Equipment.objects.get(pk=self.kwargs.get('pk', None))
        if eq is None: # TODO: 제대로 된 에러처리 필요, 404 리턴
            return None
        return EquipmentSpec.objects.filter(equipment__exact=eq).order_by('-count').first()



####################################
# History
####################################
class EquipmentHistoryListView(ListView):
    model = EquipmentHistory
    template_name = 'ems/eq_history_modal_list.html'

    def get_queryset(self):
        eq = Equipment.objects.get(pk=self.kwargs['eq_id'])
        if eq is None: # TODO: 제대로 된 에러처리 필요, 404 같은걸 리턴해야 할 듯
            return None
        
        return EquipmentHistory.objects.filter(equipment__exact=eq)
        