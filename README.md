# CASTIS ERP

- 사내 장비 관리 시스템

## 설치 방법

1. docker 설치

- CentOS 6

```sh
~$ yum install epel-release
~$ yum install docker-io git
~$ service docker start
```


- CentOS 7

```sh
~$ yum install yum-utils device-mapper-persistent-data lvm2 git
~$ yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
~$ yum install docker-ce
~$ systemctl start docker
```

- Windows
	- https://steemit.com/kr/@mystarlight/docker 참고


2. DB Migration 데이터 준비

이전에 사용하던 `MSSQL` DB 로부터 일부 table 데이터를 export 하여 이 시스템으로 migration 하는 과정이 필요하다.
각 table 에서 csv 로 export 한 후 파일명을 아래와 같이 맞춰준다.
(table 명이 기억이 나지 않는다...; column 내용을 보면 대충 어떤 table 을 export 해야 하는지 알 수 있을 것이다.)

- eq_list.csv
    - columns
        - 사번
        - 관리번호
        - 용도
        - 종류
        - 제조사
        - 모델명
        - 시리얼넘버
        - 세부사양
        - 현사용자
        - 사용용도
        - 반납예정일
        - 구입일자
        - 구입가격
        - 구입처
        - 구입요청자
        - 구매담당자
        - 장비사진
        - 관련문서

- spec.csv
    - columns
        - 사번
        - cpu
        - 메모리
        - hdd
        - 네트워크
        - graphic
        - 기타
        - 텍스트
        - 변경날짜
        - 변경사유및내역
        - 소요비용
        - 담당
        - 관련근거
        - count

- user_history.csv
    - columns
        - 사번
        - 반출일자
        - 사용자
        - 용도
        - 반납예정일
        - 반출자확인
        - 반납확인
        - 비고
        - count

- repair_history.csv
    - columns
        - 사번
        - 일자
        - 고장사유및내역
        - 처리결과
        - 비용
        - 담당
        - 관련근거
        - count

3. `장비관리시스템` 소스 다운로드

```sh
~$ git clone https://github.com/fshilver/ems.git

# 이 폴더에 위에서 만든 csv 파일 4개를 복사
# csv 파일이 없는 경우, 현재 repository 에 있는 csv 를 사용 (2018년 10월 기준 DB export 데이터)
~$ cd ems/app/fixtures/

~$ vi ems/config.env
MYSQL_DATABASE=ems         # db 이름 설정
MYSQL_ROOT_PASSWORD=castis # db root 계정 비밀번호 설정

~$ docker-compose up -d    # 실행

# docker container 내부로 진입하여 몇가지 초기화 작업이 필요
~$ docker exec -it ems-app bash  # docker container 내부 진입
~$ python3 manage.py migrate
~$ python3 manage.py createsuperuser  # 관리자용 계정을 만듭니다. email, 이름, 비밀번호 를 입력하게 됩니다.
~$ python3 manage.py collectstatic

# 복사한 csv 파일을 아래의 각 .py 스크립트가 읽어서 DB Migration
~$ cd fixtures/
~$ python3 0001_migrate_user.py
~$ python3 0002_migrate_equipment_type.py
~$ python3 0003_migrate_equipment.py
~$ python3 0004_migrate_equipment_spec.py
~$ python3 0005_migrate_equipment_history.py
~$ python3 0006_migrate_equipment_repair_history.py
~$ exit
```


4. 사이트 접속

- 브라우저로 http://서버주소/ 접속
- `python3 manage.py createsuperuser` 명령어로 생성했던 계정 정보를 입력하여 로그인
- 각 계정들의 초기 비밀번호는 castis 로 설정
- 로그인 후 오른쪽 상단에서 비밀번호 변경이 가능합니다.

> - mysql DB 접속
>   - HeidiSQL 같은 client 프로그램으로 서버주소:3306 으로 접속가능

## 재설치

재설치 시 이전에 생성했던 docker container 와 volume 이 남아있을 수 있다. 이 또한 삭제 후 설치 과정을 진행해야 깨끗하게 재설치 할 수 있다.

1. docker container 중지 및 삭제

```sh
# 현재 구동중인 docker container 확인
~$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                          PORTS               NAMES
87e75f760798        mariadb:10.3.9      "docker-entrypoint.s…"   3 days ago          Restarting (1) 15 seconds ago                       ems-db

# docker container 중지, 위 명령 출력결과에 나와있는 Names 값을 입력하거나 CONTAINER ID 사용
~$ docker stop ems-db # 또는 docker stop 87e75f760798


# -a 옵션 사용시 구동이 중지되었지만 남아있는 docker container 모두 출력
~$ docker ps -a
CONTAINER ID        IMAGE                   COMMAND                  CREATED             STATUS                          PORTS                    NAMES
bc603b0b87e0        fshilver/ems-app:0.1    "supervisord -n"         3 days ago          Exited (137) 20 hours ago                                ems-app
87e75f760798        mariadb:10.3.9          "docker-entrypoint.s…"   3 days ago          Restarting (1) 24 seconds ago                            ems-db

# docker container 삭제
~$ docker rm ems-app ems-db

# 삭제되었는지 확인
~$ docker ps -a
```

2. docker volume 삭제

ems-db container 가 사용했던 docker volume 삭제

```sh
# 생성되어 있는 docker volume 확인
~$ docker volume ls
DRIVER              VOLUME NAME
local               ems_ems-db-data

# docker volume 삭제
~$ docker volume rm ems_ems-db-data

# 삭제되었는지 확인
~$ docker volume ls
```

3. `설치방법` 의 `3번` 과정부터 다시 진행하여 재설치
