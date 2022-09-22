FROM python:3.10-slim 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN echo "yes" | python manage.py collectstatic --noinput
