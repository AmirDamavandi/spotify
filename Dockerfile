FROM python:latest

WORKDIR /project

COPY requirements.txt /project/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /project/

CMD ["gunicorn", "spotify.wsgi", "-b", "0.0.0.0:8000"]