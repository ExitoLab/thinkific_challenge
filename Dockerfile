FROM python:3.5-jessie

RUN apt-get update

RUN mkdir api

COPY . /api

WORKDIR /api

COPY requirements.txt .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]