FROM python:3.6
ENV PYTHONUNBUFFERED 2
WORKDIR /proforient
ADD requirements.txt /proforient/
RUN pip install -r requirements.txt
RUN pip install -U Django
ADD . /proforient/
