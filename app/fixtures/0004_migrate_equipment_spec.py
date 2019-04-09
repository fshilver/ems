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
from ems.models import Equipment, EquipmentSpec


def get_user_by_name(name):

    user_name = clean_user_name(name)
    
    try:
        if user_name:
            u = User.objects.get(name=user_name)
        else:
            return None
    except:
        print("fail to get user by name: '{}'".format(name))
        exit()


with open('spec.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines)

    # 0	사번
    # 1	cpu
    # 2	메모리
    # 3	hdd
    # 4	네트워크
    # 5	graphic
    # 6	기타
    # 7	텍스트
    # 8	변경날짜
    # 9	변경사유및내역
    # 10	소요비용
    # 11	담당
    # 12	관련근거
    # 13	count

    for line in lines:
        equipment_pk = line[0]
        cpu = line[1]
        mem = line[2]
        hdd = line[3]
        nic = line[4]
        grahpic = line[5]
        etc = line[6]
        text = line[7]
        change_date  = get_date(line[8])
        change_reason= line[9]
        cost         = get_price(line[10])
        change_user  = get_user_by_name(line[11])
        reference    = line[12]
        count        = int(line[13])

        try:
            eq = Equipment.objects.get(pk=equipment_pk)
        except:
            continue

        eq_spec = EquipmentSpec(equipment=eq,
                                cpu=cpu,
                                mem=mem,
                                hdd=hdd,
                                nic=nic,
                                graphic=grahpic,
                                etc=etc,
                                text=text,
                                change_date=change_date,
                                change_reason=change_reason,
                                cost=cost,
                                change_user=change_user,
                                reference=reference,
                                count=count
                                )
        eq_spec.save()
        
        