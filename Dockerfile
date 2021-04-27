FROM python:3.8


WORKDIR /usr/src/findme

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install netcat -y
RUN apt-get upgrade -y && apt-get install -y postgresql gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/usr/src/findme/entrypoint.sh"]

# FROM python:3.8
#
#
# WORKDIR /usr/src/findme
#
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
#
# COPY ./requirements.txt /usr/src/requirements.txt
# RUN pip install -r /usr/src/requirements.txt
#
# COPY . /usr/src/findme
#
# EXPOSE 8000
