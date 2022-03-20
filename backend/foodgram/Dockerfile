FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

RUN /usr/local/bin/python -m pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
CMD ["gunicorn", "foodgram.wsgi", "--bind", "0:8000" ]
