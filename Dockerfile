FROM python:3.7.4-slim
RUN apt-get update && apt-get install -y python3-dev build-essential vim git && pip install --upgrade pipenv
WORKDIR /data-resource-generator
ADD data_resource data_resource
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
ADD run.py run.py
EXPOSE 8081
RUN pipenv install && apt-get remove -y python3-dev build-essential
RUN mkdir static
RUN touch static/swagger.json
CMD ["pipenv", "run", "python", "run.py"]
