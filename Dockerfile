ARG PYTHON_VERSION=3.10.8-slim

FROM python:${PYTHON_VERSION}

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

WORKDIR /src

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src $WORKDIR


ENTRYPOINT ["python", "wsgi.py" ]


