FROM mirrors.tencent.com/eetke/tencent-python3:latest
MAINTAINER xiaoboli "xiaoboli@tencent.com"
WORKDIR /data
COPY . .
RUN apt-get install -y top ifconfig
RUN pip install -r requirements.txt
CMD ["python3", "./flask_app.py"]