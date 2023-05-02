FROM python:3.8-slim
WORKDIR /app

COPY . .

RUN pip3 install --upgrade pip

RUN pip3 install -r api_yamdb/requirements.txt --no-cache-dir

#COPY ./ /app


CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]