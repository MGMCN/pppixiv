FROM spryker/chromedriver

ENV username="username"
ENV password="password"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

RUN apk --update-cache add \
    python3 \
    py3-pip

ENTRYPOINT sh run.sh $username $password