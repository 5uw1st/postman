# coding:utf-8

from postman import create_app, celery
from postman.mail_api import mail_bp

app = create_app(logger_name="postman")

app.register_blueprint(mail_bp, url_prefix='/mail/api/v1')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
