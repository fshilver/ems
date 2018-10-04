import sys
sys.path.append('..')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'castis_erp.settings')
import django
django.setup()

import csv

from django.contrib.auth import get_user_model
from ems.models import Equipment

kind_set = set()
with open('장비목록.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines)

    for line in lines:
        if line[3]:
            kind_set.add(line[3])

from ems.models import EquipmentType

for kind in kind_set:
    e_type = EquipmentType(label=kind)
    e_type.save()