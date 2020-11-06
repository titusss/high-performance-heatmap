FROM python:3.8.5

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# COPY . /app
# WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install gunicorn

CMD exec gunicorn --bind :80 --workers 1 --threads 8 --timeout 0 app:app