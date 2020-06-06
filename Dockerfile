FROM node:14 AS node

RUN mkdir /code
WORKDIR /code

COPY package.json package-lock.json /code/
RUN npm install

COPY . /code/
RUN npm run build


FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

COPY Pipfile Pipfile.lock /code/
RUN pip install pipenv
RUN pipenv install --system

COPY . /code/
COPY --from=node /code/dist /code/

RUN python manage.py collectstatic --no-input
