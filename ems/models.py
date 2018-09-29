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