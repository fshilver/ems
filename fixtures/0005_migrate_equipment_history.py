import sys
sys.path.append('..')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'castis_erp.settings')
import django
django.setup()

import csv

from ems.models import Equipment, EquipmentHistory
import datetime

from utils import clean_user_name, name_change_map, get_date, get_price

from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_by_name(name):

    user_name = clean_user_name(name)

    if user_name == '미사용':
        return None
    
    try:
        if user_name:
            u = User.objects.get(name=user_name)
        else:
            return None
    except:
        #print("fail to get user by name: '{}' -> '{}'".format(name, user_name))
        return None


with open('사용자이력.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines)

    # 0	사번
    # 1	반출일자
    # 2	사용자
    # 3	용도
    # 4	반납예정일
    # 5	반출자확인
    # 6	반납확인
    # 7	비고
    # 8	count

    for line in lines:
        equipment_pk = line[0]
        check_out_date = get_date(line[1])
        user = get_user_by_name(line[2])
        purpose = line[3]
        check_in_duedate = get_date(line[4])
        manager_confirm = line[5]
        check_in_confirm = line[6]
        note = line[7]
        count = int(line[8])
        
        try:
            eq = Equipment.objects.get(pk=equipment_pk)
        except:
            #print("장비ID({})가 존재하지 않습니다. 해당 내용은 migration 되지 않습니다.".format(equipment_pk))
            continue

        eq_history = EquipmentHistory(equipment=eq,
                                    check_out_date=check_out_date,
                                    user=user,
                                    purpose=purpose,
                                    check_in_duedate=check_in_duedate,
                                    manager_confirm=manager_confirm,
                                    check_in_confirm=check_in_confirm,
                                    note=note,
                                    count=count,
                                    )
        eq_history.save()
