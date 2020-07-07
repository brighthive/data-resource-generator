FROM python:3.7.4-slim
WORKDIR /data-resource-generator

# RUN apt-get update && apt-get install -y python3-dev build-essential vim git gunicorn
# RUN pip install --upgrade pip
# RUN pip install pipenv
# RUN pip install --upgrade pipenv gevent

RUN apt-get update && apt-get install -y python3-dev build-essential git &&\
    pip install --upgrade pipenv
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN pipenv install --system &&\
    apt-get remove -y python3-dev build-essential

ADD cmd.sh cmd.sh
RUN chmod +x cmd.sh
ADD wsgi.py wsgi.py

RUN mkdir static
RUN touch static/swagger.json

ADD data_resource data_resource

EXPOSE 8081
ENTRYPOINT ["/data-resource-generator/cmd.sh"]
