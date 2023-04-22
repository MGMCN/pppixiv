FROM zyuzka/chromedriver:latest

ENV username="username"
ENV password="password"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

ENTRYPOINT sh run.sh $username $password