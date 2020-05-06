FROM mirrors.tencent.com/eetke/tencent-python3:latest
MAINTAINER xiaoboli "xiaoboli@tencent.com"
WORKDIR /data
COPY . .
RUN rm -rf /etc/apt/sources.list.d && apt-get clean all && apt-get update && apt-get install -y top ifconfig
RUN pip install -r requirements.txt
CMD ["python3", "./flask_app.py"]