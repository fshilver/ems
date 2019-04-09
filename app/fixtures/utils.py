import datetime

# 현재사용자가 팀명 또는 구분하기 어려운 이름으로 되어 있는 경우
# 특정 사용자로 변경

admin_name = '캐스트이즈'

# 'eq_list.csv'-'현사용자' column
change_map_for_current_user = {
    'FD': admin_name,
    'KT': '구자윤B',
    'QM': admin_name,
    'SN': admin_name,
    '공용': admin_name,
    '분실': admin_name,
    '경영관리팀': admin_name,
    '이경훈': '이경훈A',
    '구자윤': '구자윤A',
}

# 'eq_list.csv'-'구입요청자' column
change_map_for_purchase_requester = {
    'AD. 김대기': '김대기',
    'AD이차원': '이차원',
    'AD정준용': '정준용',
    'AD최은주': '최은주',
    'B.이창섭': '이창섭',
    'B김한성': '김한성',
    'B이상철': '이상철',
    'B조배두': '조배두',
    'CEO.김승학': '김승학',
    'CEO김승학': '김승학',
    'CTO.박종관': '박종관',
    'CTO박종관': '박종관',
    'FD박태욱': '박태욱',
    'FD양인자': '양인자',
    'FD천광규': '천광규',
    'M. 박준호': '박준호',
    'M.박준호': '박준호',
    'M박준호': '박준호',
    'M정선민': '정선민',
    'PSN주인호': '주인호',
    'PS김영건': '김영건',
    'PS이유미': '이유미',
    'QM안재훈': '안재훈',
    'QM이재근': '이재근',
    'SD박훈': '박훈',
    'SD김영태': '김영태',
    'SD윤상훈': '윤상훈',
    'SE김종혁': '김종혁',
    'SN김종혁': '김종혁',
    'SN박정석': '박정석',
    'SPD강호종': '강호종',
    'SW임대섭': '임대섭',
    'TFT박태욱': '박태욱',
    'UX이혜연': '이혜연',
    '황인수수석': '황인수',
    '김승학사장님': '김승학',
    '전무님': '박종관',
    '차경호': '차정호', # 차정호 님 오타인듯
    '구자윤': '구자윤A', # 동일한 이름은 A 로 통일
    '양경모': '양경모A', # 동일한 이름은 A 로 통일
}

# 'eq_list.csv'-'구매담당자' column
change_map_for_purchase_manager = {
    'M. 조용장': '조용장',
    'M.조용장': '조용장',
    'M김재봉': '김재봉',
    'M하상원': '하상원',
    'B조배두': '조배두',
    'M정선민': '정선민',
    '경영관리팀': '정선민', # 구매담당자가 경영관리팀으로 되어 있는 경우 정선민 으로 변경
}


# 'repair_history.csv'-'담당' column
change_map_for_repair_history = {
    'SN김정훈': '김정훈',
    'AD이하나': '이하나',
    'AD장필수': '장필수',
    '손망실보고서': admin_name,
}

# 'user_history.csv'-'사용자' column
change_map_for_user_history = {
    '12명': admin_name,
    '경영전략실': admin_name,
    '공통': admin_name,
    '김종혁, 최아연': '김종혁',
    '사장님실 옆 창가1': admin_name,
    '사장님실 옆 창가2': admin_name,
    '신입사원': admin_name,
    '아이티네이드': admin_name,
    '양희성(SE팀 전체)': '양희성',
    '전체': admin_name,
    '전체(최상화)': '최상화',
    '정우영, 강호종': '정우영',
    '타업체': admin_name,
    '팀': admin_name,
    'KT_TFT': '구자윤B',
}

name_change_map = {}
name_change_map.update(change_map_for_current_user)
name_change_map.update(change_map_for_purchase_manager)
name_change_map.update(change_map_for_purchase_requester)
name_change_map.update(change_map_for_repair_history)
name_change_map.update(change_map_for_user_history)

active_email_address = {
    admin_name: 'castis@castis.com',
    '강신애': 'chlksa@castis.com',
    '강현종': 'khj0119@castis.com',
    '고은혜': 'eunhyeco@castis.com',
    '구자윤A': 'kooja0418@castis.com',
    '구자윤B': 'abid0917@castis.com',
    '권현오': 'kho625@castis.com',
    '김경길': 'whoau@castis.com',
    '김경송': 'kskim@castis.com',
    '김경하': 'magic4417@castis.com',
    '김경환': 'tomkim@castis.com',
    '김광일': 'kgi8789@castis.com',
    '김규석': 'kskim0428@castis.com',
    '김대기': 'elitekim@castis.com',
    '김대현': 'salme4@castis.com',
    '김덕윤': 'kimdy@castis.com',
    '김민규': 'mk613@castis.com',
    '김민기': 'kmk6868@castis.com',
    '김수향': 'tid105@castis.com',
    '김승학': 'shkim@castis.com',
    '김시원': 'steamcool@castis.com',
    '김영건': 'radiohead@castis.com',
    '김영훈': 's1m2m@castis.com',
    '김응진': 'zx7498@castis.com',
    '김인표': 'kip2056@castis.com',
    '김재기': 'jacky2845@castis.com',
    '김재진': 'jjkim@castis.com',
    '김정훈': 'kjunghoon@castis.com',
    '김진아': 'jinakim@castis.com',
    '김진영': 'jy0528@castis.com',
    '김태호': 'hoya2352@castis.com',
    '김혜미': 'hmkim@castis.com',
    '김효원': 'hyowonk@castis.com',
    '문광석': 'ansrhkd00@castis.com',
    '박성규': 'psknim@castis.com',
    '박정석': 'boynpark@castis.com',
    '박종관': 'jkpark@castis.com',
    '박준석': 'bobmann@castis.com',
    '박지수': 'jisuuu4@castis.com',
    '박지영': 'jypark1329@castis.com',
    '박찬성': '2zumin@castis.com',
    '박훈': 'sinma@castis.com',
    '배정환': 'psybank@castis.com',
    '서수빈': 'tjtn1234@castis.com',
    '서양덕': 'ydseo@castis.com',
    '서현준': 'forbunz@castis.com',
    '성석진': 'spearmint@castis.com',
    '성아현': 'julia1129@castis.com',
    '손동희': 'son1113@castis.com',
    '손정현': 'hook20@castis.com',
    '신석균': 'skshin@castis.com',
    '안재훈': 'jhahn@castis.com',
    '안종찬': 'ahnchan2@castis.com',
    '양경모A': 'kmyang@castis.com',
    '양경모B': 'croce@castis.com',
    '양인자': 'graisle@castis.com',
    '양희성': 'hsyang@castis.com',
    '염정준': 'jun3045@castis.com',
    '오강현': 'ganghyeon@castis.com',
    '원수연': 'wsy1470@castis.com',
    '유동현': 'donghyun@castis.com',
    '유선우': 'sunwooyou@castis.com',
    '육지현': 'salvame527@castis.com',
    '윤기선': 'alexyun@castis.com',
    '윤상훈': 'dahakan@castis.com',
    '윤시헌': 'flower91611@castis.com',
    '윤영열': 'yyyun@castis.com',
    '이가람': 'ygr980@castis.com',
    '이경훈A': 'puyo0223@castis.com',
    '이경훈B': 'centuerion@castis.com',
    '이기수': 'kslee@castis.com',
    '이대희': 'baramvv@castis.com',
    '이동은': 'masterkey@castis.com',
    '이두란': 'duran1230@castis.com',
    '이미희': 'maizi@castis.com',
    '이상윤': 'sangyoon@castis.com',
    '이상호': 'sorry249@castis.com',
    '이수웅': 'cr7@castis.com',
    '이승건': 'sg0314@castis.com',
    '이승준': 'lsj99@castis.com',
    '이영주': 'mdk20000@castis.com',
    '이원희': 'lwh@castis.com',
    '이윤경': 'lyk0513@castis.com',
    '이은진': 'dmswls750@castis.com',
    '이재근': 'goodido@castis.com',
    '이재범': 'uttntt@castis.com',
    '이준우': 'jacklee@castis.com',
    '이지선': 'elmo90@castis.com',
    '이지연': 'jiyun0610@castis.com',
    '이진형': 'leejh@castis.com',
    '이차원': 'ah2dius@castis.com',
    '이하나': 'ehana0210@castis.com',
    '이현규': 'leehyunguu@castis.com',
    '이현서': 'hs6956@castis.com',
    '이현지': 'ehyeong@castis.com',
    '이혜연': 'idhy2000@castis.com',
    '임대섭': 'daeseob@castis.com',
    '임동현': 'dhlim@castis.com',
    '임수진': 'bstar46@castis.com',
    '임종진': 'zxcvbvcxz@castis.com',
    '임창성': 'hellolcs@castis.com',
    '임태환': 'intro309@castis.com',
    '장성훈': 'mistymemory@castis.com',
    '장세연': 'sasgas@castis.com',
    '장재석': 'jsjang@castis.com',
    '장필수': 'jjangpil@castis.com',
    '전성우': 'swjun@castis.com',
    '전성환': 'shane@castis.com',
    '정다을': 'jde0731@castis.com',
    '정다혜': 'jdaun0406@castis.com',
    '정동진': 'jdj85@castis.com',
    '정선민': 'sm1984@castis.com',
    '정성종': 'sjchung@castis.com',
    '정순진': 'jsj1005@castis.com',
    '정영찬': 'jyc123@castis.com',
    '정재헌': 'jjh@castis.com',
    '정재훈': 'sian475@castis.com',
    '정종호': 'jongho45@castis.com',
    '조영탁': 'clavis909@castis.com',
    '조영혁': 'choyh@castis.com',
    '조은혜': 'zzowooneh@castis.com',
    '주재성': 'ju8625@castis.com',
    '지행진': 'jhj@castis.com',
    '진광현': 'chiphy@castis.com',
    '차정호': 'polkmji12@castis.com',
    '천광규': 'chonkk@castis.com',
    '최동혁': 'cdh3063@castis.com',
    '최성언': 'suchoi13@castis.com',
    '최수지': 'ssuji389@castis.com',
    '최영화': 'mooby84@castis.com',
    '최은주': 'iuwe1126@castis.com',
    '최정문': 'wjdans0172@castis.com',
    '최종석': 'choijs007@castis.com',
    '최훈서': 'hunseo11@castis.com',
    '하태진': 'htj1222@castis.com',
    '한지윤': 'awesomehan77@castis.com',
    '황소연': 'soyeon01@castis.com',
    '황인창': 'hic@castis.com',
    '황인천': 'dotmany@castis.com',
    '황진주': 'pearlhwang@castis.com',
    '윤성우': 'ysw0721@castis.com',
}


def clean_user_name(name):
    
    if name == '':
        return None

    if name == '미사용':
        return None

    if name == '\\N':
        return None

    if name == ', ':
        return None

    if name == ', ,':
        return None

    if name == ', , ':
        return None

    if ( '/' in name ):
        user_name = (name.split('/'))[-1].strip()
    else:
        user_name = name

    if user_name in name_change_map:
        user_name = name_change_map[user_name]

    # 구자윤b -> 구자윤B
    user_name = user_name.upper()
    
    return user_name
    

def get_date(text):
    '''
    legacy 데이터 중에 '2017-07-' 과 같은 비정상적인 데이터가 있음
    이에 대한 처리도 해줌

    2017-02-30 과 같은 없는 날짜도 존재함
    이런 데이터는 9999-12-31 로 설정
    '''
    if text == '':
        return None
    
    try:
        yyyy, mm, dd = text.split('-')

        yyyy = int(yyyy) if yyyy != '' else 9999
        mm = int(mm) if mm != '' else 1
        dd = int(dd) if dd != '' else 1

    except ValueError:
        return datetime.date(9999,12,31)

    try:
        date = datetime.date(yyyy, mm, dd)
    except ValueError:
        date = datetime.date(9999,12,31)

    return date


def get_price(text):
    if text == '':
        return 0

    if text == '무료':
        return 0

    if text == 'ㅇ':
        return 0
    
    try:
        return int(text.replace(',',''))
    except ValueError:
        return 0
