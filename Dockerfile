FROM python:3.11-alpine

ENV DJANGO_ENV=production

RUN mkdir /app

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/music_school

RUN python manage.py collectstatic --noinput

RUN python manage.py makemigrations

RUN python manage.py migrate

EXPOSE 8001

CMD [ "daphne", "-p", "8001", "-b", "0.0.0.0", "music_school.asgi:application" ]