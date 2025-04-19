FROM python:latest

WORKDIR /project

COPY requirements.txt /project/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /project/
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "spotify.wsgi", "-b", "0.0.0.0:8000"]