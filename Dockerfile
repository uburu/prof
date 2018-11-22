FROM python:3.6
ENV PYTHONUNBUFFERED 2
WORKDIR /proforient
RUN pip install -U Django
ADD . /proforient/
CMD docker-compose up
