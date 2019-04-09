import sys
import os
import django
import csv
import datetime
from django.contrib.auth import get_user_model

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'castis_erp.settings.development')
django.setup()
User = get_user_model()

from ems.models import Equipment, EquipmentType

kind_set = set()
with open('eq_list.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines)

    for line in lines:
        if line[3]:
            kind_set.add(line[3])

for kind in kind_set:
    e_type = EquipmentType(label=kind)
    e_type.save()
