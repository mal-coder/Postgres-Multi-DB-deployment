FROM python:3.8-slim-buster
RUN pip install pipenv

ENV PYTHONUNBUFFERED 1

WORKDIR  .

ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system --deploy

COPY . .
COPY . /app
COPY . /tools


CMD ["python", "app/main.py"]
