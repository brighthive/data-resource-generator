FROM python:3.7.4-slim
RUN apt-get update && apt-get install -y python3-dev build-essential vim git gunicorn postgresql postgresql-contrib && pip install --upgrade pipenv gevent
WORKDIR /data-resource-generator
ADD data_resource data_resource
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
ADD wsgi.py wsgi.py
EXPOSE 8081
RUN pipenv install && apt-get remove -y python3-dev build-essential
RUN mkdir static
RUN touch static/swagger.json
ADD cmd.sh cmd.sh
RUN chmod +x cmd.sh
ENTRYPOINT ["/data-resource-generator/cmd.sh"]
