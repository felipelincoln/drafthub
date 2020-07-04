FROM node:14 AS node

RUN mkdir -p /code/src
WORKDIR /code

COPY package.json package-lock.json /code/
RUN npm install

COPY ./src /code/src
COPY ./webpack.config.js /code

RUN npm run css-build
RUN npm run js-build


FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system

COPY . /code/
COPY --from=node /code/static /code/static

RUN python manage.py collectstatic --no-input
