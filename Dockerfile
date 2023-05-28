FROM python:3.11

LABEL maintainer="Ali Negary <github.com/ali-negary>"

RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . /app
ENV FLASK_APP=src.app
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]