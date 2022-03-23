FROM python:3.8-slim

EXPOSE 8000

WORKDIR /app

COPY backend/foodgram/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]