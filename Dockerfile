FROM zyuzka/chromedriver:100

ENV username="username"
ENV password="password"
ENV gfw="0"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

ENTRYPOINT sh run.sh $username $password $gfw