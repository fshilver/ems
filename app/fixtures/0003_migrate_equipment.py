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

from utils import name_change_map
from ems.models import Equipment, EquipmentType


def get_user_by_name(name):

    if name == '': # 빈 값은 미사용으로
        return None

    if name == '미사용':
        return None

    if ( '/' in name ):
        user_name = (name.split('/'))[-1].strip()
    else:
        user_name = name

    if user_name in name_change_map:
        user_name = name_change_map[user_name]

    # 구자윤b -> 구자윤B
    user_name = user_name.upper()
    unused = '미사용'

    if user_name == unused:
        return None
    
    try:
        u = User.objects.get(name=user_name)
    except:
        print("get user by name: '{}'".format(name))
        print(user_name)
        print(user_name.encode('utf-8'))
        print(unused.encode('utf-8'))
        exit()

    return u


def get_kind(name):
    if name == '':
        return None
    
    return EquipmentType.objects.get(label=name)


def get_accessibility(text):
    text = text.strip()
    if text == '개인용':
        return Equipment.PRIVATE
    elif text == '공용':
        return Equipment.PUBLIC
    else:
        return None

def get_date(text):
    '''
    legacy 데이터 중에 '2017-07-' 과 같은 비정상적인 데이터가 있음
    이에 대한 처리도 해줌

    2017-02-30 과 같은 없는 날짜도 존재함
    이런 데이터는 9999-12-31 로 설정
    '''
    if text == '':
        return None
    
    yyyy, mm, dd = text.split('-')

    if yyyy != '':
        yyyy = int(yyyy)
    else:
        9999

    if mm != '':
        mm = int(mm)
    else:
        mm = 1

    if dd != '':
        dd = int(dd)
    else:
        dd = 1

    try:
        date = datetime.date(yyyy, mm, dd)
    except ValueError:
        date = datetime.date(9999,12,31)

    return date


def get_price(text):
    if text == '':
        return 0
    else:
        return int(text.replace(',',''))


with open('eq_list.csv', encoding='euc-kr') as f:
    # 0	사번
    # 1	관리번호
    # 2	용도
    # 3	종류
    # 4	제조사
    # 5	모델명
    # 6	시리얼넘버
    # 7	세부사양
    # 8	현사용자
    # 9	사용용도
    # 10	반납예정일
    # 11	구입일자
    # 12	구입가격
    # 13	구입처
    # 14	구입요청자
    # 15	구매담당자
    # 16	장비사진
    # 17	관련문서
    lines = csv.reader(f)
    next(lines) # skip first line
    for line in lines:
        pk = int(line[0])
        management_number = line[1].strip()
        accessibility = get_accessibility(line[2])
        kind = get_kind(line[3])
        manufacturer = line[4].strip()
        model = line[5].strip()
        serial_number = line[6].strip()
        current_user = get_user_by_name(line[8])
        purpose = line[9].strip()
        check_in_duedate = get_date(line[10])
        purchase_date = get_date(line[11])
        price = get_price(line[12])
        buying_shop = line[13].strip()
        purchase_request_user = get_user_by_name(line[14])
        purchase_manager = get_user_by_name(line[15])
        document = line[17]

        if current_user is not None:
            status = Equipment.USED
        else:
            status = Equipment.USABLE

        e = Equipment(pk=pk, management_number=management_number, accessibility=accessibility, kind=kind, manufacturer=manufacturer, model=model, serial_number=serial_number, current_user=current_user, purpose=purpose, check_in_duedate=check_in_duedate, purchase_date=purchase_date, price=price, buying_shop=buying_shop, purchase_request_user=purchase_request_user, purchase_manager=purchase_manager, document=document, status=status)
        e.save()
