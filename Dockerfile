FROM python:3.10-slim 
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN sh -c "echo \"yes\" | python manage.py collectstatic --noinput"
