FROM nfqlt/chromedriver:latest

ENV username="username"
ENV password="password"
ENV port="5000"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

RUN apt-get update -y && \
    apt-get install python3-pip -y && \
    pip3 install --break-system-packages -r requirements.txt

ENTRYPOINT sh run.sh $username $password $port