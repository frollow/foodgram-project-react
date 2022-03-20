FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .
CMD ["gunicorn", "foodgram.wsgi", "--bind", "0:8000" ]
