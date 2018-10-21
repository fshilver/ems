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
)
import json

####################################
# Equipment
####################################
def update_equipment_status(request, status, user=None):
    """
    ajax api. 동시에 여러개의 장비 상태를 변경할 수 있다.
    """
    if request.is_ajax():
        if request.method == 'POST':
            ids = request.POST.getlist('ids[]')

            for id in ids:
                eq = Equipment.objects.get(id=id)
                eq.status = status

                if user:
                    # 사용하는 사람 '없음' 으로 변경
                    if user == 'null':
                        eq.current_user = None
                    else:
                        eq.current_user = user

                eq.save()

            message = "{}번 장비 상태 변경 성공".format(','.join(ids))
            context = {
                'message': message
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'error': '{} is unsupported method'.format(request.method)})
    else:
        return JsonResponse({'error': 'This is not a ajax request'})


def apply_use_eq(request):
    """
    장비 사용 신청
    사용 신청 시 Equipment.current_user 는 요청자가 되어야 한다.
    """
    return update_equipment_status(request, Equipment.WAITING_FOR_ACCEPT_TO_USE, request.user)


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
    사용 신청 반송 시 Equipment.current_user 는 다시 None 이 되어야 한다.
    """
    return update_equipment_status(request, Equipment.USABLE, 'null')


def apply_return_eq(request):
    """
    장비 반납 신청
    반납 신청 시 Equipment.current_user 는 이미 설정되어 있다.
    """
    print("장비 반납 승인 대기중...")
    return update_equipment_status(request, Equipment.WAITING_FOR_ACCEPT_TO_RETURN)


def accept_return_eq(request):
    """
    장비 반납 신청 승인
    반납 후 Equipment.current_user 는 None 이 되어야 한다.
    """
    return update_equipment_status(request, Equipment.USABLE, 'null')


def reject_return_eq(request):
    """
    장비 반납 신청 반송
    반납 신청 반송 시 Equipment.current_user 는 이미 설정되어 있었으므로 변경할 필요 없다.
    """
    return update_equipment_status(request, Equipment.USED)


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

