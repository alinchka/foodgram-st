FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0:8000", "foodgram.wsgi:application"] 