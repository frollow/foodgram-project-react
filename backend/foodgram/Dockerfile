FROM python:3.7-slim

EXPOSE 8000

WORKDIR /app

COPY /requirements.txt .

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
