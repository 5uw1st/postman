# coding:utf-8


from postman import create_app, celery

app = create_app()
app.app_context().push()
