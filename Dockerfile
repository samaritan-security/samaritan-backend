FROM ubuntu:latest

MAINTAINER Samaritan Security "sdmay20-45@iastate.edu"

RUN apt-get update -y

RUN apt-get install -y python3-pip python-dev build-essential

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
