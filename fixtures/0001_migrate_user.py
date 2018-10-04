import sys
sys.path.append('..')
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'castis_erp.settings')
import django
django.setup()

import csv
#from castis_erp.fixtures.utils import clean_user_name, active_email_address
from utils import clean_user_name, active_email_address

user_name_set = set()


# 현재 사용자
with open('장비목록.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines) # skip first line

    for line in lines:
        user_name_set.add(clean_user_name(line[8])) # '현재사용자'
        user_name_set.add(clean_user_name(line[14])) # '구입요청자'
        user_name_set.add(clean_user_name(line[15])) # '구입담당자'

with open('사용자이력.csv', encoding='euc-kr') as f:
    lines = csv.reader(f)
    next(lines)

    for line in lines:
        user_name_set.add(clean_user_name(line[2]))

deactive_email_address = {}

n = 1
for user_name in user_name_set:

    if user_name == '미사용':
        continue

    if user_name is None:
        continue

    if user_name == '':
        continue

    if user_name not in active_email_address:
        print("add to deactive user:{},retiree{}@castis.com".format(user_name, n))
        deactive_email_address[user_name] = 'retiree{}@castis.com'.format(n)
        n += 1


from django.contrib.auth import get_user_model
User = get_user_model()

for user_name in active_email_address:
    u = User.objects.create_user(active_email_address[user_name], user_name, password='castis')
    print("create user:{},{}".format(user_name,active_email_address[user_name]))
    u.is_active = True
    u.is_staff = False
    u.save()


for user_name in deactive_email_address:
    u = User.objects.create_user(deactive_email_address[user_name], user_name, password='castis')
    print("create user:{},{}".format(user_name,deactive_email_address[user_name]))
    u.is_active = False
    u.is_staff = False
    u.save()