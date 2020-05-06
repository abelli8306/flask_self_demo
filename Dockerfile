FROM python:3.7
MAINTAINER xiaoboli "xiaoboli@tencent.com"
# 配置腾讯apt-get源，使用的是 debian 10.2
COPY ./build/sources.list /etc/apt/sources.list
RUN rm -rf /etc/apt/sources.list.d && apt-get clean all && apt-get update && apt-get install -y vim build-essential top ifconfig

# 配置腾讯pip源
RUN mkdir -p .pip
COPY ./build/pip.conf /root/.pip/pip.conf

WORKDIR /data
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "./flask_app.py"]