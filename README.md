邮件服务：
===
1.项目介绍：
---
 - **背景**：现各个项目中都需要邮件服务，但都是自己各自实现，为满足此需求，故设计一个邮件服务，提供一个restful接口。

2.项目依赖：
---
 - python3.6
 - redis
 - mongodb
 - celery
 - flask
 - flower

3.日志目录：
---
    /var/log/postman/
    
4.部署：
---
1.Build Dockerfile：
```bash
docker build -f Dockerfile . -t postman:v1
```
2.Run email api:
```bash
docker run -d --name="postman_api" --env FLASK_CONFIG="config.ProdConfig" --env REDIS_URI="redis://10.8.10.128:6379/1" --env MONGODB_URI="mongodb://10.8.10.128:27017/spider" -v $(pwd):/opt/spider/postman/ -v /var/log/postman:/var/log/postman -p 9001:9000 postman:v1 python manage.py
```
3.Run celery worker:
```bash
docker run -d --name="postman_worker" --env FLASK_CONFIG="config.ProdConfig" --env REDIS_URI="redis://10.8.10.128:6379/1" --env MONGODB_URI="mongodb://10.8.10.128:27017/spider" -v $(pwd):/opt/spider/postman/ -v /var/log/postman:/var/log/postman postman:v1 celery worker -A celery_worker.celery -l INFO -f /var/log/postman/worker.log
```
4.Run flower:
```bash
docker run -d --name="postman_flower" -p 5556:5555 postman:v1 flower --port 5555 --broker=redis://10.8.10.128:6379/1
```



