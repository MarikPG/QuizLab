FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); u, _ = User.objects.get_or_create(username='David', defaults={'email': 'admin@example.com'}); u.set_password('AdminPass123!'); u.is_superuser = True; u.is_staff = True; u.save()\" && gunicorn quizlab.wsgi:application --bind 0.0.0.0:8000"]