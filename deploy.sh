#!/usr/bin/env bash

docker build -f Dockerfile . -t postman:v1
docker run -d --name="postman_api" --env FLASK_CONFIG="config.ProdConfig" --env REDIS_URI="redis://10.8.10.128:6379/1" --env MONGODB_URI="mongodb://10.8.10.128:27017/spider" -v $(pwd):/opt/spider/postman/ -v /var/log/postman:/var/log/postman -p 9001:9000 postman:v1 python manage.py

docker run -d --name="postman_worker" --env FLASK_CONFIG="config.ProdConfig" --env REDIS_URI="redis://10.8.10.128:6379/1" --env MONGODB_URI="mongodb://10.8.10.128:27017/spider" -v $(pwd):/opt/spider/postman/ -v /var/log/postman:/var/log/postman postman:v1 celery worker -A celery_worker.celery -l INFO -f /var/log/postman/worker.log

docker run -d --name="postman_flower" -p 5556:5555 postman:v1 flower --port 5555 --broker=redis://10.8.10.128:6379/1