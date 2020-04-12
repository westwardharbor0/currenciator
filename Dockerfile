FROM alpine

ENV FLASK_APP=api.py
ENV API_PORT=3692

RUN apk upgrade --no-cache \
  && apk add --no-cache \
    python3 \
  && pip3 install --no-cache-dir --upgrade pip \
  && rm -rf /var/cache/* \
  && rm -rf /root/.cache/*

COPY . /currenciator

WORKDIR /currenciator

RUN pip3 install -r requirements.txt

CMD flask run --port $API_PORT