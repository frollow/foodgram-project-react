FROM python:3.8-slim

EXPOSE 8000

COPY backend/foodgram/requirements.txt .
RUN python pip install -r backend/foodgram/requirements.txt

WORKDIR /app
COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]