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

from utils import clean_user_name, name_change_map, get_date, get_price
from ems.models import Equipment, EquipmentRepairHistory


def get_user_by_name(name):

    user_name = clean_user_name(name)

    if user_name == '미사용':
        return None
    
    try:
        if user_name:
            u = User.objects.get(name=user_name)
            return u
        else:
            return None
    except:
        #print("fail to get user by name: '{}' -> '{}'".format(name, user_name))
        return None


with open('repair_history.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines)

    # 0	사번
    # 1	일자
    # 2	고장사유및내역
    # 3	처리결과
    # 4	비용
    # 5	담당
    # 6	관련근거
    # 7	count
    for line in lines:
        equipment_pk = line[0]
        date = get_date(line[1])
        reason = line[2]
        result = line[3]
        cost = get_price(line[4])
        manager = get_user_by_name(line[5])
        reference = line[6]
        count = int(line[7])

        try:
            eq = Equipment.objects.get(pk=equipment_pk)
        except:
            #print("장비ID({})가 존재하지 않습니다. 해당 내용은 migration 되지 않습니다.".format(equipment_pk))
            continue

        eq_repair_history = EquipmentRepairHistory(equipment=eq,
                                                    date=date,
                                                    reason=reason,
                                                    result=result,
                                                    cost=cost,
                                                    manager=manager,
                                                    reference=reference,
                                                    count=count
                                                    )
        eq_repair_history.save()
