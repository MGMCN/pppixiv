FROM nfqlt/chromedriver:latest

ENV username="user_wwvg5583"
ENV password="nizuiai357"
ENV port="5000"

LABEL maintainer="MGMCN"

USER root

COPY . /APP

WORKDIR /APP

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --break-system-packages -r requirements.txt && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT sh run.sh $username $password $port

docker run -d -p 3333:5001 -e username="user_wwvg5583" -e password="nizuiai357"  -v ./APP/Illusts godmountain/pppixiv:latest