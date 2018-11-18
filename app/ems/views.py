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
    EquipmentReturn,
)
from .forms import (
    EquipmentSpecForm,
    EquipmentForm,
    EquipmentUpdateForm,
    EquipmentApplyForm,
    EquipmentRejectForm,
    EquipmentReturnForm,
    EquipmentRejectReturnForm,
    EquipmentCheckOutForm,
)
import re
import datetime


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
    queryset = EquipmentApply.objects.filter(status=EquipmentApply.APPLIED)

    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            if self.object_list:
                for obj in self.object_list:
                    eq_data = {
                        'id': obj.id,
                        'equipment_id': obj.equipment.id,
                        'management_number': obj.equipment.management_number,
                        'status': obj.get_status_display(),
                        'serial_number': obj.equipment.serial_number,
                        'model': obj.equipment.model,
                        'requester': obj.user.name,
                        'check_in_duedate': obj.check_in_duedate,
                        'purpose': obj.purpose,
                        'apply_date': obj.apply_date,
                    }
                    data.append(eq_data)
            return JsonResponse({'data': data})

        return super().render_to_response(context)



class EquipmentApplyFormListView(ListView):
    """
    장비 사용 신청 이력
    """
    model = EquipmentApply
    template_name = 'ems/eq_apply_form_list.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return EquipmentApply.objects.filter(user=self.request.user)
        return super().get_queryset()


    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            if self.object_list:
                for obj in self.object_list:
                    eq_data = {
                        'id': obj.id,
                        'equipment_id': obj.equipment.id,
                        'management_number': obj.equipment.management_number,
                        'status': obj.get_status_display(),
                        'serial_number': obj.equipment.serial_number,
                        'model': obj.equipment.model,
                        'requester': obj.user.name,
                        'check_in_duedate': obj.check_in_duedate,
                        'purpose': obj.purpose,
                        'apply_date': obj.apply_date,
                        'reject_reason': obj.reject_reason,
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



def reject_eq_form_view(request):
    """
    장비 사용 신청 거절 modal form
    """
    template_name = 'modal_form.html'

    if request.method == "POST":
        form = EquipmentRejectForm(request.POST)

        if form.is_valid():
            raw_string = form.cleaned_data.get('apply_form_list') # string : ['1549,1548,1547'] 
            apply_form_id_list = re.sub("[\[\]']", '', raw_string).split(',') # -> list : ['1549', '1548', '1547']

            for id in apply_form_id_list:
                with transaction.atomic():
                    apply_form = EquipmentApply.objects.select_for_update().get(pk=id) # TODO: ORM 개선, 404 처리
                    apply_form.reject_reason = form.cleaned_data.get('reject_reason')
                    apply_form.status = EquipmentApply.DISAPPROVED

                    eq = apply_form.equipment
                    eq.status = Equipment.USABLE

                    apply_form.save()
                    eq.save()
            return redirect('ems:apply_eq_list')
        else:
            return render(request, template_name, context={"form": form})
    else:
        form = EquipmentRejectForm(initial=request.GET)
    return render(request, template_name, context={"form": form})


def checkout_eq_form_view(request):
    """
    장비 사용 승인 modal form (관리자용 : 승인 절차 없이 바로 처리)
    """
    if request.method == "POST":
        form = EquipmentCheckOutForm(request.POST)

        if form.is_valid():
            raw_string = form.cleaned_data.get('equipment_list') # string : ['1549,1548,1547'] 
            eq_id_list = re.sub("[\[\]']", '', raw_string).split(',') # -> list : ['1549', '1548', '1547']

            for id in eq_id_list:
                with transaction.atomic():

                    eq = Equipment.objects.select_for_update().get(pk=id, status=Equipment.USABLE) # TODO: ORM 개선, 404 처리

                    # 장비 정보 변경
                    eq.status = Equipment.USED
                    eq.current_user = form.cleaned_data.get('user')
                    eq.purpose = form.cleaned_data.get('purpose')
                    eq.check_in_duedate = form.cleaned_data.get('check_in_duedate')

                    # 장비 이력 생성
                    eq_history = EquipmentHistory(user=eq.current_user
                                                ,equipment=eq
                                                ,purpose=eq.purpose
                                                ,check_in_duedate=eq.check_in_duedate
                                                ,note=form.cleaned_data.get('note')
                                                ,check_out_date=datetime.date.today()
                    )
                    eq.save()
                    eq_history.save()
            return redirect('ems:eq_list')
        else:
            return render(request, "modal_form.html", context={"form": form})
        
    else:
        # use initial value for hidden field(equipment_list) from get params : ?equipment_list=10,11
        # in this case, get param name and hidden field name is same(equipment_list)
        form = EquipmentCheckOutForm(initial=request.GET)
    return render(request, "modal_form.html", context={"form": form})



def return_eq_form_view(request):
    """
    장비 반납 신청 modal form
    """
    if request.method == "POST":
        form = EquipmentReturnForm(request.POST)

        if form.is_valid():
            raw_string = form.cleaned_data.get('equipment_list') # string : ['1549,1548,1547'] 
            eq_id_list = re.sub("[\[\]']", '', raw_string).split(',') # -> list : ['1549', '1548', '1547']

            for id in eq_id_list:
                with transaction.atomic():
                    eq = Equipment.objects.select_for_update().get(pk=id, status=Equipment.USED) # TODO: ORM 개선, 404 처리
                    eq.status = Equipment.WAITING_FOR_ACCEPT_TO_RETURN
                    eq.save()
                    eq_return = EquipmentReturn(user=request.user
                                                ,equipment=eq
                                                ,reason=form.cleaned_data['reason']
                                                ,note=form.cleaned_data['note']
                    )
                    eq_return.save()
            return redirect('ems:used_eq_list')
        else:
            return render(request, "modal_form.html", context={"form": form})
        
    else:
        # use initial value for hidden field(equipment_list) from get params : ?equipment_list=10,11
        # in this case, get param name and hidden field name is same(equipment_list)
        form = EquipmentReturnForm(initial=request.GET)
    return render(request, "modal_form.html", context={"form": form})



def reject_return_eq_form_view(request):
    """
    장비 반납 신청 거절 modal form
    """
    template_name = 'modal_form.html'

    if request.method == "POST":
        form = EquipmentRejectReturnForm(request.POST)

        if form.is_valid():
            raw_string = form.cleaned_data.get('return_form_list') # string : ['1549,1548,1547'] 
            return_form_id_list = re.sub("[\[\]']", '', raw_string).split(',') # -> list : ['1549', '1548', '1547']

            for id in return_form_id_list:
                with transaction.atomic():
                    return_form = EquipmentReturn.objects.select_for_update().get(pk=id) # TODO: ORM 개선, 404 처리
                    return_form.reject_reason = form.cleaned_data.get('reject_reason')
                    return_form.status = EquipmentReturn.DISAPPROVED

                    eq = return_form.equipment
                    eq.status = Equipment.USED

                    return_form.save()
                    eq.save()
            return redirect('ems:return_eq_list')
        else:
            return render(request, template_name, context={"form": form})
    else:
        form = EquipmentRejectReturnForm(initial=request.GET)
    return render(request, template_name, context={"form": form})



def checkin_eq_form_view(request):
    """
    장비 반납 신청 modal form (관리자용 : 승인 절차 없이 바로 반납 처리)
    """
    if request.method == "POST":
        form = EquipmentReturnForm(request.POST)

        if form.is_valid():
            raw_string = form.cleaned_data.get('equipment_list') # string : ['1549,1548,1547'] 
            eq_id_list = re.sub("[\[\]']", '', raw_string).split(',') # -> list : ['1549', '1548', '1547']

            for id in eq_id_list:
                with transaction.atomic():
                    eq_queryset = Equipment.objects.select_for_update().filter(pk=id, status=Equipment.USED) | Equipment.objects.select_for_update().filter(pk=id, status=Equipment.WAITING_FOR_ACCEPT_TO_RETURN) # TODO: ORM 개선, 404 처리
                    eq = eq_queryset.first()

                    # 장비 이력 수정
                    eq_history = EquipmentHistory.objects.select_for_update().filter(user=eq.current_user).filter(equipment=eq).last()
                    eq_history.check_in_confirm = '반납완료' # TODO: 반납 확인자로 바꿔야 할 듯

                    # 장비 정보 변경
                    eq.status = Equipment.USABLE
                    eq.current_user = None

                    eq.save()
                    eq_history.save()

            return redirect('ems:eq_list')
        else:
            return render(request, "modal_form.html", context={"form": form})
        
    else:
        # use initial value for hidden field(equipment_list) from get params : ?equipment_list=10,11
        # in this case, get param name and hidden field name is same(equipment_list)
        form = EquipmentReturnForm(initial=request.GET)
    return render(request, "modal_form.html", context={"form": form})



class ReturnEquipmentListView(ListView):
    """
    반납 신청한 장비 목록
    """
    model = EquipmentReturn
    template_name = 'ems/return_eq_list.html'


    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model._default_manager.filter(status=EquipmentReturn.APPLIED)
        else:
            return self.model._default_manager.filter(status=EquipmentReturn.APPLIED).filter(user=self.request.user)


    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            if self.object_list:
                for obj in self.object_list:
                    eq_data = {
                        'id': obj.id,
                        'equipment_id': obj.equipment.id,
                        'management_number': obj.equipment.management_number,
                        'status': obj.get_status_display(),
                        'serial_number': obj.equipment.serial_number,
                        'model': obj.equipment.model,
                        'requester': obj.user.name,
                        'reason': obj.reason,
                        'apply_date': obj.apply_date,
                    }
                    data.append(eq_data)
            return  JsonResponse({'data': data})

        return super().render_to_response(context)



class EquipmentReturnFormListView(ListView):
    """
    장비 반납 신청 이력
    """
    model = EquipmentReturn
    template_name = 'ems/eq_return_form_list.html'

    def get_queryset(self):
        if not self.request.user.is_superuser:
            return self.model._default_manager.filter(user=self.request.user)
        return super().get_queryset()


    def render_to_response(self, context):
        if self.request.is_ajax():
            data = []
            if self.object_list:
                for obj in self.object_list:
                    eq_data = {
                        'id': obj.id,
                        'equipment_id': obj.equipment.id,
                        'management_number': obj.equipment.management_number,
                        'status': obj.get_status_display(),
                        'serial_number': obj.equipment.serial_number,
                        'model': obj.equipment.model,
                        'requester': obj.user.name,
                        'reason': obj.reason,
                        'apply_date': obj.apply_date,
                        'reject_reason': obj.reject_reason,
                    }
                    data.append(eq_data)
            return JsonResponse({'data': data})

        return super().render_to_response(context)



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
        