FROM python:latest

WORKDIR /spotify_project

COPY requirements.txt /spotify_project/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /spotify_project/
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "spotify.wsgi", "-b", "0.0.0.0:8000"]