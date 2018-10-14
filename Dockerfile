FROM python:3
MAINTAINER Andrey Varfolomeev 
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.test.txt /code/
COPY requirements.heroku.txt /code/
COPY requirements.txt /code/
RUN pip install -r requirements.test.txt
COPY . /code/

CMD ["sh", "start.sh"]
