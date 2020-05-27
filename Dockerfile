FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
RUN mkdir /code/staticfiles
RUN touch /code/staticfiles/.live
RUN mkdir /code/staticfiles/css
RUN mkdir /code/staticfiles/img
RUN mkdir /code/staticfiles/js
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv && pipenv install --system

COPY . /code/
