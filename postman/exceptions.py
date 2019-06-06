# coding:utf-8


class CustomError(Exception):
    code = 1001
    msg = "处理失败"

    def __init__(self, msg=None, extra_msg=None):
        if msg:
            self.msg = msg
        if extra_msg:
            self.msg += ", {0}".format(extra_msg)

    def __str__(self):
        return "{0}, code:{1}, msg: {2}".format(self.__class__.__name__, self.code, self.msg)


class ApiError(CustomError):
    code = 2001
    msg = "处理API请求失败"


class LackParamError(ApiError):
    code = 2002
    msg = "请求缺少必要参数"


class ParamTypeError(ApiError):
    code = 2003
    msg = "请求参数类型错误"


class ResultTypeError(ApiError):
    code = 2004
    msg = "返回结果类型错误"


class ConfigNotExist(ApiError):
    code = 2005
    msg = "配置信息不存在"


class TaskNotExist(ApiError):
    code = 2006
    msg = "任务不存在"
