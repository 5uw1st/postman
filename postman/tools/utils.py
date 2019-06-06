# coding:utf-8

import binascii
import datetime
import os
import uuid
from hashlib import md5

from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder


def get_current_time(format_str=None, utc=False, ret_date=True):
    format_str = format_str or "%Y-%m-%d %X"
    t = datetime.datetime.utcnow() if utc else datetime.datetime.now()
    return t if ret_date else t.strftime(format_str)


def format_time(time_obj, format_str=None):
    format_str = format_str or "%Y-%m-%d %X"
    return time_obj.strftime(format_str)


def get_uuid(ret_hex=False):
    uid = uuid.uuid1()
    return uid.get_hex() if ret_hex else str(uid)


def get_md5(text):
    """
    获取文本MD5值
    :param text: string/bytes
    :return: string
    """
    if isinstance(text, str):
        text = text.encode()
    return md5(text).hexdigest()


def generate_config_key(project):
    """
    生产配置key
    :param project: string
    :return: str
    """
    rnd_bytes = os.urandom(16)
    return get_md5(b"_".join([project.encode(), rnd_bytes]))[::-1]


def generate_aes_encrypt_key(config_key):
    """
    生成AES加密秘钥
    :param config_key: str 配置key
    :return: str
    """
    rnd_bytes = os.urandom(16)
    return get_md5(b"_".join([rnd_bytes, config_key.encode()]))[::-1]


def encrypt_aes(message, key, iv):
    """
    AES加密
    :param message: 消息内容
    :param key: 加密key
    :param iv: 加密iv
    :return: 加密文本
    """
    message = PKCS7Encoder().encode(message)
    cipher = AES.new(key, AES.MODE_CBC, iv[:16])
    encrypted_value = cipher.encrypt(message)
    return binascii.hexlify(encrypted_value).decode('utf8')


def decrypt_aes(text, key, iv):
    """
    AES解密
    :param text: 加密文本
    :param key: 加密key
    :param iv: 加密iv
    :return: 消息内容
    """
    cipher = AES.new(key, mode=AES.MODE_CBC, IV=iv[:16])
    decrypted_value = cipher.decrypt(binascii.unhexlify(text)).decode()
    unpad = lambda s: s[0:-ord(s[-1])]
    return unpad(decrypted_value)


if __name__ == '__main__':
    msg = "Hello World"
    key = "5e739bb8de7a11e89f9af0def1a8a8e7"
    iv = key
    text = encrypt_aes(message=msg, key=key, iv=iv)
    print(text)

    m = decrypt_aes(text, key, iv)
    print(m)
