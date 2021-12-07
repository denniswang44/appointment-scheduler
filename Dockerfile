# syntax=docker/dockerfile:1

FROM python:3.9.9
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=flaskr
RUN flask init-db
CMD ["flask", "run"]