# coding:utf-8

from celery.utils.log import get_task_logger
from postman.tools.utils import get_current_time
import json
from postman import celery
from postman.models import TaskInfo

logger = get_task_logger(__name__)


class TaskStatus(object):
    TODO = "TODO"
    DOING = "DOING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


class MyTask(celery.Task):

    def __init__(self, log=None):
        self.logger = log or logger
        self.task_id = ""
        self.task_name = ""
        super(MyTask, self).__init__()

    def delay(self, *args, **kwargs):
        task_id = kwargs.pop("task_id", "")
        self.insert_task(task_id=task_id, args=args, kwargs=kwargs)
        return self.apply_async(args, kwargs, task_id=task_id)

    def on_success(self, retval, task_id, args, kwargs):
        self.logger.info('task done: {0}'.format(retval))
        self.update_task_status(task_id=task_id, status=TaskStatus.SUCCESS, result=retval)
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.logger.info('task fail, reason: {0}'.format(exc))
        self.update_task_status(task_id=task_id, status=TaskStatus.FAILED, error_msg=einfo)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def insert_task(self, task_id, args, kwargs):
        task_info = {
            "task_id": task_id,
            "task_name": self.task_name,
            "args": list(args),
            "kwargs": kwargs,
            "status": TaskStatus.TODO
        }
        TaskInfo(**task_info).save()
        self.logger.info("===>>>>Insert a new task, task_id: {0}, task_name:{1}".format(task_id, self.task_name))

    def update_task_status(self, task_id, status, result=None, error_msg=None):
        """
        更新任务状态
        :param task_id: 任务ID
        :param status: 任务状态
        :param result: 任务结果
        :param error_msg: 错误信息
        :return:
        """
        task_obj = TaskInfo.objects(task_id=task_id).first()
        if task_obj:
            task_obj.update(set__status=status, result=self.format_data(result), error_msg=self.format_data(error_msg),
                            task_name=self.task_name, update_time=get_current_time())
            self.logger.info(
                "===>>>>update task status, task_id:{2} | <{0} ===> {1}>".format(task_obj.status, status, task_id))
        else:
            self.logger.warning(">>>This task has not existed, task_id:{0}".format(task_id))

    @staticmethod
    def format_data(data):
        """
        格式化数据
        :param data:
        :return:
        """
        if data is None:
            return ""
        elif isinstance(data, dict):
            return json.dumps(data)
        else:
            return str(data)
