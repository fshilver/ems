from django.http import JsonResponse, HttpResponse
from .models import Equipment

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

                if eq.current_user is None and user is not None:
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
    신청 승인 시 Equipment.current_user 는 이미 설정되어 있다.
    """
    return update_equipment_status(request, Equipment.USED)


def reject_use_eq(request):
    """
    장비 사용 신청 반송
    사용 신청 반송 시 Equipment.current_user 는 다시 None 이 되어야 한다.
    """
    return update_equipment_status(request, Equipment.USABLE, None)


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
    return update_equipment_status(request, Equipment.USABLE, None)


def reject_return_eq(request):
    """
    장비 반납 신청 반송
    반납 신청 반송 시 Equipment.current_user 는 이미 설정되어 있었으므로 변경할 필요 없다.
    """
    return update_equipment_status(request, Equipment.USED)