FROM alpine
RUN apk upgrade --no-cache \
  && apk add --no-cache \
    python3 \
    python3-pip \
  && pip3 install --no-cache-dir --upgrade pip \
  && rm -rf /var/cache/* \
  && rm -rf /root/.cache/*

RUN cd /usr/bin \
  && ln -sf python3 python \
  && ln -sf pip3 pip

COPY . /currenciator

RUN export FLASK_APP=/currenciator/api.py
RUN flask run