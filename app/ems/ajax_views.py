from django.db import transaction
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseNotAllowed,
)
from django.shortcuts import get_object_or_404
from .models import (
    Equipment,
    RepairStatus,
    EquipmentType,
    EquipmentApply,
    EquipmentHistory,
    EquipmentReturn,
)
import json
import datetime

####################################
# Equipment
####################################
def accept_use_eq(request):
    """
    장비 사용 신청 승인
    1. 장비 상태 변경
    2. 장비 이력 생성
    3. applyform 상태 변경(승인)
    """
    if request.method == "POST":
        data_list = json.loads(request.body)

        for data in data_list:
            with transaction.atomic():
                eq = Equipment.objects.select_for_update().get(pk=data.get('equipment_id'))
                apply_form = EquipmentApply.objects.select_for_update().get(pk=data.get('apply_form_id'))

                # 장비 정보 변경
                eq.status = Equipment.USED
                eq.current_user = apply_form.user
                eq.purpose = apply_form.purpose
                eq.check_in_duedate = apply_form.check_in_duedate

                # 장비 이력 생성
                eq_history = EquipmentHistory(user=apply_form.user
                                            ,equipment=eq
                                            ,purpose=apply_form.purpose
                                            ,check_in_duedate=apply_form.check_in_duedate
                                            ,note=apply_form.note
                                            ,check_out_date=datetime.date.today()
                )

                # applyform 상태 변경
                apply_form.status = EquipmentApply.APPROVED
                eq.save()
                eq_history.save()
                apply_form.save()

        return JsonResponse({'message': '성공'})
        
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


def reject_use_eq(request):
    """
    장비 사용 신청 반송
    1. 장비 상태 변경
    2. applyform 상태 변경(승인)
    """
    if request.method == "POST":
        data_list = json.loads(request.body)

        for data in data_list:
            with transaction.atomic():
                # 장비 상태 변경
                eq = Equipment.objects.select_for_update().get(pk=data.get('equipment_id'), status=Equipment.WAITING_FOR_ACCEPT_TO_USE)
                eq.status = Equipment.USABLE

                # applyform 상태 변경
                apply_form = EquipmentApply.objects.select_for_update().get(pk=data.get('apply_form_id'))
                apply_form.status = EquipmentApply.DISAPPROVED

                eq.save()
                apply_form.save()

        return JsonResponse({'message': '성공'})
        
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


def cancel_apply_eq(request):
    """
    장비 사용 신청 취소
    1. 장비 상태 변경
    2. applyform 상태 변경(승인)
    """
    if request.method == "POST":
        data_list = json.loads(request.body)

        for data in data_list:
            with transaction.atomic():
                # 장비 상태 변경
                eq = Equipment.objects.select_for_update().get(pk=data.get('equipment_id'), status=Equipment.WAITING_FOR_ACCEPT_TO_USE)
                eq.status = Equipment.USABLE

                # applyform 상태 변경
                apply_form = EquipmentApply.objects.select_for_update().get(pk=data.get('apply_form_id'))
                apply_form.status = EquipmentApply.CANCELED

                eq.save()
                apply_form.save()

        return JsonResponse({'message': '성공'})
        
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


def cancel_return_eq(request):
    """
    장비 반납 신청 취소
    1. 장비 상태 변경
    2. returnform 상태 변경
    """
    if request.method == "POST":
        data_list = json.loads(request.body)

        for data in data_list:
            with transaction.atomic():
                # 장비 상태 변경
                eq = Equipment.objects.select_for_update().get(pk=data.get('equipment_id'), status=Equipment.WAITING_FOR_ACCEPT_TO_RETURN)
                eq.status = Equipment.USED

                # returnform 상태 변경
                return_form = EquipmentReturn.objects.select_for_update().get(pk=data.get('return_form_id'))
                return_form.status = EquipmentReturn.CANCELED

                eq.save()
                return_form.save()

        return JsonResponse({'message': '성공'})
        
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


def accept_return_eq(request):
    """
    장비 반납 신청 승인
    1. 장비 상태 변경: USABLE
    2. 장비 이력 수정: 반납일시, 반납확인
    3. applyform 상태 변경
    """
    if request.method == "POST":
        data_list = json.loads(request.body)

        for data in data_list:
            with transaction.atomic():
                eq = Equipment.objects.select_for_update().get(pk=data.get('equipment_id'))
                return_form = EquipmentReturn.objects.select_for_update().get(pk=data.get('return_form_id'))

                # 장비 정보 변경
                eq.status = Equipment.USABLE
                eq.current_user = None

                # 장비 이력 수정
                eq_history = EquipmentHistory.objects.select_for_update().filter(user=return_form.user).filter(equipment=eq).last()
                eq_history.check_in_confirm = '반납완료' # TODO: 반납 확인자로 바꿔야 할 듯

                # returnform 상태 변경
                return_form.status = EquipmentReturn.APPROVED
                eq.save()
                eq_history.save()
                return_form.save()

        return JsonResponse({'message': '성공'})
        
    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


def change_status_eq(request):
    if request.method == 'POST':
        status = request.POST.get('status_code', None)
        if status is None:
            return JsonResponse({'error': 'invalid status code'})

        ids = request.POST.getlist('ids[]')
        for id in ids:
            eq = get_object_or_404(Equipment, pk=id)
            eq.status = status
            eq.save()

        return JsonResponse({'message': '상태 변경 성공'})

    return JsonResponse({'error': '{} is unsupported method'.format(request.method)})


####################################
# RepairStatus 
####################################
def delete_repair_status(request):
    """
    동시에 여러개의 '수리상태' label 을 삭제할 수 있다.
    """
    if request.is_ajax():
        if request.method == 'POST':
            ids = request.POST.getlist('ids[]')

            for id in ids:
                status = RepairStatus.objects.get(id=id)
                status.delete()

            message = "{}번 삭제 성공".format(','.join(ids))
            context = {
                'message': message
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'error': '{} is unsupported method'.format(request.method)})
    else:
        return JsonResponse({'error': 'This is not a ajax request'})


####################################
# EquipmentType 
####################################
def delete_equipment_type(request):
    """
    동시에 여러개의 '장비종류' label 을 삭제할 수 있다.
    """
    if request.is_ajax():
        if request.method == 'POST':
            ids = request.POST.getlist('ids[]')

            for id in ids:
                status = EquipmentType.objects.get(id=id)
                status.delete()

            message = "{}번 삭제 성공".format(','.join(ids))
            context = {
                'message': message
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'error': '{} is unsupported method'.format(request.method)})
    else:
        return JsonResponse({'error': 'This is not a ajax request'})

