FROM spryker/chromedriver

ENV username="username"
ENV password="password"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

RUN apk --update-cache add \
    python3 \
    python3-dev \
    py3-pip \
    gcc \
    g++ \
    curl \
    bash && \
    pip3 install -r requirements.txt && \
    rm -rf .env && \
    touch .env

ENTRYPOINT sh run.sh $username $password