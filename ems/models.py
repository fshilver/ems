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

    serial_number    = models.CharField(max_length=50,verbose_name='시리얼넘버')
    purchase_date    = models.DateField(verbose_name='구입일자', null=True)
    price = models.IntegerField(verbose_name='구입가격')
    status = models.SmallIntegerField(choices=STATUS, default=USABLE,verbose_name='상태')

    management_number = models.CharField(max_length=50, verbose_name='관리번호')
    accessibility = models.CharField(max_length=50, choices=ACCESSIBILITY, default=PRIVATE, verbose_name='용도')
    kind = models.ForeignKey(EquipmentType, on_delete=models.SET_NULL, null=True,verbose_name='종류')
    manufacturer = models.CharField(max_length=50,verbose_name='제조사')
    model = models.CharField(max_length=50,verbose_name='모델')
    purpose = models.TextField(verbose_name='사용용도')
    check_in_duedate = models.DateField(verbose_name='반납예정일', null=True)
    buying_shop = models.CharField(max_length=50, verbose_name='구입처', blank=True, null=True)
    purchase_manager = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='purchase_manager', verbose_name='구매담당자')
    document = models.CharField(max_length=100, verbose_name='관련문서')

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
    cost         = models.IntegerField(verbose_name='소요비용')
    change_user  = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='change_user', verbose_name='담당')
    reference    = models.CharField(max_length=50, blank=True, null=True, verbose_name='관련근거')
    count        = models.SmallIntegerField(verbose_name='Count')


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


class EquipmentRepairHistory(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date      = models.DateField(verbose_name='일자')
    reason    = models.TextField(verbose_name='고장사유및내역')
    result    = models.CharField(max_length=100, verbose_name='처리결과')
    cost      = models.IntegerField(verbose_name='비용')
    manager   = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, verbose_name='담당자')
    reference = models.CharField(max_length=50, blank=True, null=True, verbose_name='관련근거')
    count     = models.SmallIntegerField(verbose_name='Count')
