FROM python:3.8-bullseye

WORKDIR /app

COPY api_yamdb/requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY api_yamdb/ /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
