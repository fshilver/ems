FROM ubuntu:16.04
MAINTAINER fshilver@gmail.com

RUN sed -i 's/archive\.ubuntu/kr\.archive\.ubuntu/' /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    nginx \
    supervisor \
    language-pack-ko \
    libmysqlclient-dev \
    sqlite3 && \
    pip3 install -U pip setuptools && \
    rm -rf /var/lib/apt/lists/*

RUN locale-gen ko_KR.UTF-8
ENV LANG=ko_KR.UTF-8 LANGUAGE=ko_KR.UTF-8 LC_ALL=ko_KR.UTF-8

RUN pip3 install uwsgi

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/sites-available/default
COPY supervisor.conf /etc/supervisor/conf.d/

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.

COPY requirements/* /home/docker/code/requirements/
RUN pip3 install -r /home/docker/code/requirements/production.txt

ENV DJANGO_SETTINGS_MODULE castis_erp.settings.production

COPY . /home/docker/code/
WORKDIR /home/docker/code/app/


CMD ["supervisord", "-n"]
