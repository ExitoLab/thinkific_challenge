FROM python:3.5-jessie

ENV http_proxy="http://switcher:Alpha.02%@172.25.20.215:80"
ENV https_proxy="http://switcher:Alpha.02%@172.25.20.215:80"

RUN apt-get update

RUN mkdir api

COPY . /api

WORKDIR /api

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]