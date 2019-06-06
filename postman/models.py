# coding:utf-8

from datetime import datetime

from postman import mongodb as db


class EmailConfig(db.Document):
    """
    邮件配置信息
    """
    project = db.StringField(max_length=30)
    config_key = db.StringField(required=True)
    mail_to = db.ListField(db.EmailField(), required=True)
    mail_from = db.EmailField(required=True)
    mail_host = db.StringField(required=True)
    mail_port = db.IntField(required=True)
    mail_user = db.StringField()
    mail_pwd = db.StringField(required=True)
    mail_cc = db.ListField(db.EmailField())
    aes_encrypt_key = db.StringField(required=True, max_length=32)
    create_time = db.DateTimeField(default=datetime.now())
    update_time = db.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'postman.emailConfigInfo',
        'ordering': ['-update_time'],
        'strict': False,
    }


class TaskInfo(db.Document):
    """
    任务信息
    """
    task_id = db.StringField(required=True)
    task_name = db.StringField()
    status = db.StringField(required=True)
    error_msg = db.StringField()
    result = db.StringField()
    args = db.ListField()
    kwargs = db.DictField()
    create_time = db.DateTimeField(default=datetime.now())
    update_time = db.DateTimeField(default=datetime.now())

    meta = {
        'collection': 'postman.taskInfo',
        'ordering': ['-update_time'],
        'strict': False,
    }
