# coding:utf-8

from flask import Blueprint, current_app

from postman.exceptions import ConfigNotExist, LackParamError, TaskNotExist
from postman.models import EmailConfig, TaskInfo
from postman.tasks.email import do_send_mail
from postman.tools.decorators import parse_request
from postman.tools.utils import get_current_time, generate_config_key, generate_aes_encrypt_key, \
    decrypt_aes, get_uuid, format_time

mail_bp = Blueprint("mail_api", __name__)


@mail_bp.route('/test', methods=['GET', 'POST'])
def test():
    return "Hello World"


@mail_bp.route('/update_config', methods=['POST'])
@parse_request()
def update_config(request):
    """
    更新邮件配置信息
    :param request: 请求对象
    :return: dict
    """
    request_data = request.json
    config_key = request_data.get("config_key")
    project = request_data.get("project", "")
    request_data.pop("aes_encrypt_key", "")
    if config_key:
        # 更新配置信息
        current_app.logger.info("==>Need update config info, project:{0}, key:{1}".format(project, config_key))
        # 查询原有信息
        config_info = EmailConfig.objects(config_key=config_key).first()
        if not config_info:
            raise ConfigNotExist(extra_msg=config_key)
        fields = config_info._fields.keys()
        new_info = dict()
        for field in fields:
            if field in ("_id", "config_key", "aes_encrypt_key", "update_time", "create_time"):
                continue
            value = request_data.get(field)
            if value is not None:
                new_info[field] = value
        new_info["update_time"] = get_current_time()
        config_info.update(__raw__={"$set": new_info})
        return {"msg": "更新配置信息成功"}
    else:
        # 添加配置信息
        config_key = generate_config_key(project=project)
        aes_key = generate_aes_encrypt_key(config_key=config_key)
        current_app.logger.info("==>Need add a new config info, project:{0}, key:{1}".format(project, config_key))
        request_data.update({"config_key": config_key, "aes_encrypt_key": aes_key})
        EmailConfig(**request_data).save()
        return {"msg": "添加配置信息成功", "config_key": config_key, "aes_encrypt_key": aes_key}


@mail_bp.route('/send_mail', methods=['POST'])
@parse_request()
def send_mail(request):
    """
    发送邮件
    :param request: 请求对象
    :return: dict
    """
    request_data = request.json
    config_key = request_data.get("config_key")
    subject = request_data.get("subject")
    message = request_data.get("message")
    if not all([config_key, subject, message]):
        raise LackParamError
    # 获取配置信息
    config_info = EmailConfig.objects(config_key=config_key).first()
    if not config_info:
        raise ConfigNotExist(extra_msg=config_key)
    sub_type = request_data.get("sub_type", "plain")
    has_encrypt = request_data.get("encrypt", False)
    charset = request_data.get("charset", "utf-8")
    real_message = decrypt_aes(text=message, key=config_key, iv=config_key) if has_encrypt else message
    mail_info = {
        "mail_from": config_info.mail_from,
        "mail_to": config_info.mail_to,
        "mail_host": config_info.mail_host,
        "mail_port": config_info.mail_port,
        "mail_user": config_info.mail_user or config_info.mail_from,
        "mail_pwd": config_info.mail_pwd,
        "subject": subject,
        "message": real_message,
        "sub_type": sub_type,
        "charset": charset,
    }
    task_id = get_uuid()
    do_send_mail.delay(mail_info, task_id=task_id)
    return {"msg": "已添加至队列，后台发送中", "task_id": task_id}


@mail_bp.route('/get_result', methods=['POST'])
@parse_request()
def get_result(request):
    """
    获取任务结果
    :param request: 请求对象
    :return: dict
    """
    request_data = request.json
    task_id = request_data.get("task_id")
    task_info = TaskInfo.objects(task_id=task_id).first()
    if not task_info:
        raise TaskNotExist
    ret_info = {
        "status": task_info.status,
        "result": task_info.result,
        "error_msg": task_info.error_msg,
        "create_time": format_time(task_info.create_time),
        "update_time": format_time(task_info.update_time),
    }
    return ret_info
