FROM python:3.6
MAINTAINER liuli, liuli6@dianrong.com

ENV WORK_DIR=/opt/spider/postman \
    LOG_PATH=/var/log/postman

RUN mkdir -p ${WORK_DIR} ${LOG_PATH}

# 设置时区
RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo 'Asia/Shanghai' >/etc/timezone

WORKDIR ${WORK_DIR}

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
ADD . .