from django.db import models
from django.contrib.auth import get_user_model

class RepairStatus(models.Model):
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label


class EquipmentType(models.Model):
    label = models.CharField(max_length=10)

    def __str__(self):
        return self.label


class Equipment(models.Model):
    current_user          = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='current_user')
    purchase_request_user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='purchase_request_user')

    serial_number    = models.CharField(max_length=50)
    purchase_date    = models.DateField()
    price = models.IntegerField()

    def __str__(self):
        return self.serial_number


class EquipmentSpec(models.Model):
    equipment    = models.OneToOneField(Equipment, on_delete=models.CASCADE)
    cpu          = models.CharField(max_length=50, blank=True, null=True)
    mem          = models.CharField(max_length=50, blank=True, null=True)
    hdd          = models.CharField(max_length=50, blank=True, null=True)
    nic          = models.CharField(max_length=50, blank=True, null=True)
    graphic      = models.CharField(max_length=50, blank=True, null=True)
    manufacturer = models.CharField(max_length=50, blank=True, null=True)
