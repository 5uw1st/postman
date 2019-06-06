# coding:utf-8

from celery.utils.log import get_task_logger

from postman import celery
from postman.tasks import MyTask
from postman.tools.mailer import EmailSender

logger = get_task_logger(__name__)


@celery.task(base=MyTask, bind=True, name="send_mail")
def do_send_mail(self, mail_info):
    logger.info('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(self.request))
    logger.info('Send message from {0} to {1}'.format(mail_info["mail_from"], mail_info["mail_to"]))
    with EmailSender(mail_info["mail_user"], mail_info["mail_pwd"], server=mail_info["mail_host"],
                     port=mail_info["mail_port"]) as m:
        msg = {
            "msg": mail_info["message"],
            "from": mail_info["mail_from"],
            "subject": mail_info["subject"]
        }
        ret = m.send_mail(mail_info["mail_from"], mail_info["mail_to"], msg, sub_type=mail_info["sub_type"],
                          charset=mail_info["charset"])
        logger.info("===>Send email {0}".format("successful" if ret else "failed"))
        return ret
