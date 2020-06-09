FROM node:14 AS node

RUN mkdir -p /code/src/sass
WORKDIR /code

COPY package.json package-lock.json /code/
RUN npm install

COPY ./src/sass /code/src/sass

RUN npm run css-build


FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system

COPY . /code/
COPY --from=node /code/static/css/ /code/static/css/

RUN python manage.py collectstatic --no-input
