from django.db import models
from django.contrib.auth import get_user_model
import datetime


class RepairStatus(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class EquipmentType(models.Model):
    label = models.CharField(max_length=10)

    class Meta:
        unique_together = ('id', 'label')

    def __str__(self):
        return self.label


class Equipment(models.Model):

    # STATUS 코드
    USABLE = 0
    WAITING_FOR_ACCEPT_TO_USE = 10
    WAITING_FOR_ACCEPT_TO_RETURN = 11
    USED = 20

    STATUS = (
        (USABLE, '사용 가능'),
        (USED, '사용 중'),
        (WAITING_FOR_ACCEPT_TO_USE, '사용 승인 대기 중'),
        (WAITING_FOR_ACCEPT_TO_RETURN, '반납 승인 대기 중'),
    )

    # ACCESSIBILITY 코드
    PRIVATE = 0
    PUBLIC = 1
    ACCESSIBILITY = (
        (PRIVATE, '개인용'),
        (PUBLIC, '공용'),
    )

    current_user          = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='current_user', verbose_name='현재 사용자')
    purchase_request_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='purchase_request_user', verbose_name='구입요청자')

    serial_number    = models.CharField(max_length=50, verbose_name='시리얼넘버', blank=True, null=True)
    purchase_date    = models.DateField(verbose_name='구입일자', blank=True, null=True)
    price = models.IntegerField(verbose_name='구입가격', blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS, default=USABLE,verbose_name='상태')

    management_number = models.CharField(max_length=50, verbose_name='관리번호')
    accessibility = models.SmallIntegerField(choices=ACCESSIBILITY, default=PRIVATE, verbose_name='용도')
    kind = models.ForeignKey(EquipmentType, on_delete=models.SET_NULL, null=True, verbose_name='종류')
    manufacturer = models.CharField(max_length=50, verbose_name='제조사', blank=True, null=True)
    model = models.CharField(max_length=50, verbose_name='모델', blank=True, null=True)
    purpose = models.TextField(verbose_name='사용용도')
    check_in_duedate = models.DateField(verbose_name='반납예정일', blank=True, null=True)
    buying_shop = models.CharField(max_length=50, verbose_name='구입처', blank=True, null=True)
    purchase_manager = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='purchase_manager', verbose_name='구매담당자')
    document = models.CharField(max_length=100, verbose_name='관련문서', blank=True, null=True)

    class Meta:
        unique_together = ('serial_number', 'management_number')


    def __str__(self):
        return self.serial_number


class EquipmentSpec(models.Model):
    equipment    = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    cpu          = models.CharField(max_length=50, blank=True, null=True, verbose_name='CPU')
    mem          = models.CharField(max_length=50, blank=True, null=True, verbose_name='메모리')
    hdd          = models.CharField(max_length=50, blank=True, null=True, verbose_name='HDD')
    nic          = models.CharField(max_length=50, blank=True, null=True, verbose_name='네트워크')
    graphic      = models.CharField(max_length=50, blank=True, null=True, verbose_name='Graphic')
    etc          = models.CharField(max_length=50, blank=True, null=True, verbose_name='기타')
    text         = models.CharField(max_length=50, blank=True, null=True, verbose_name='텍스트')

    # 별도의 클래스로 분리 필요
    change_date  = models.CharField(max_length=50, blank=True, null=True, verbose_name='변경날짜')
    change_reason= models.CharField(max_length=50, blank=True, null=True, verbose_name='변경사유및내역')
    cost         = models.IntegerField(verbose_name='소요비용', blank=True, null=True)
    change_user  = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,blank=True, null=True, related_name='change_user', verbose_name='담당')
    reference    = models.CharField(max_length=50, blank=True, null=True, verbose_name='관련근거')
    count        = models.SmallIntegerField(verbose_name='Count', blank=True, null=True)


class EquipmentHistory(models.Model):
    equipment        = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    check_out_date   = models.DateField(verbose_name='반출일자', null=True)
    user             = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='사용자')
    purpose          = models.CharField(max_length=50, verbose_name='용도', null=True)
    check_in_duedate = models.DateField(verbose_name='반납예정일', null=True)
    manager_confirm  = models.CharField(max_length=20, verbose_name='반출자확인', null=True)
    check_in_confirm = models.CharField(max_length=20, verbose_name='반납확인', null=True)
    note             = models.TextField(verbose_name='비고', null=True)
    count            = models.SmallIntegerField(verbose_name='Count', null=True)

    class Meta:
        ordering = ['check_out_date']


class EquipmentRepairHistory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date      = models.DateField(verbose_name='일자')
    reason    = models.TextField(verbose_name='고장사유및내역')
    result    = models.CharField(max_length=100, verbose_name='처리결과')
    cost      = models.IntegerField(verbose_name='비용')
    manager   = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='담당자')
    reference = models.CharField(max_length=50, blank=True, null=True, verbose_name='관련근거')
    count     = models.SmallIntegerField(verbose_name='Count')


class EquipmentApply(models.Model):

    # STATUS 코드
    APPLIED = 0
    APPROVED = 10
    DISAPPROVED = 20
    CANCELED = 30

    STATUS = (
        (APPLIED, '사용 신청 검토중'), # FIXME: 문자열 변경 시 eq_apply_form_list.html 의 '사용신청' 부분도 같이 변경해줘야 함. 현재로선 더 나은 방법을 모르겠음
        (APPROVED, '사용 승인'),
        (DISAPPROVED, '사용 거절'),
        (CANCELED, '사용 신청 취소'),
    )
    apply_date = models.DateField(auto_now_add=True, verbose_name="사용신청일")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="사용신청자")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="신청장비")
    purpose = models.TextField(verbose_name="사용 목적")
    check_in_duedate = models.DateField(verbose_name="반납 예정일")
    note = models.TextField(verbose_name="기타", blank=True, null=True)
    reject_reason = models.TextField(verbose_name="사용 신청 거절 이유", blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS, default=APPLIED, verbose_name="상태")


class EquipmentReturn(models.Model):

    # STATUS 코드
    APPLIED = 0
    APPROVED = 10
    DISAPPROVED = 20
    CANCELED = 30

    STATUS = (
        (APPLIED, '반납 신청 검토중'), # FIXME: 문자열 변경 시 eq_apply_form_list.html 의 '사용신청' 부분도 같이 변경해줘야 함. 현재로선 더 나은 방법을 모르겠음
        (APPROVED, '반납 승인'),
        (DISAPPROVED, '반납 거절'),
        (CANCELED, '반납 신청 취소'),
    )
    apply_date = models.DateField(auto_now_add=True, verbose_name="반납신청일")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="반납신청자")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name="신청장비")
    reason = models.TextField(verbose_name="반납사유")
    note = models.TextField(verbose_name="기타", blank=True, null=True)
    reject_reason = models.TextField(verbose_name="반납신청 거절이유", blank=True, null=True)
    status = models.SmallIntegerField(choices=STATUS, default=APPLIED, verbose_name="상태")
