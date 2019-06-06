# coding:utf-8

from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP


class EmailSender(object):

    def __init__(self, username, password, server=None, port=None, timeout=None):
        self._server_host = server
        self._port = port
        self.timeout = timeout or 10
        self.__mail_server = None
        self.__username = username
        self.__password = password

    def __conn_server(self):
        if not self.__mail_server:
            self.__mail_server = SMTP(self._server_host, self._port, self.timeout)

    def _login(self, mail_from, mail_password):
        self.__mail_server.starttls()
        self.__mail_server.login(mail_from, mail_password)

    def send_mail(self, mail_from, mail_to, mail_message, sub_type="plain", charset="utf-8"):
        if not isinstance(mail_message, dict):
            return False
        message = MIMEText(mail_message.get("msg"), sub_type, charset)
        message['From'] = Header(mail_message.get("from"))
        message['Subject'] = Header(mail_message.get("subject"), charset)
        self.__mail_server.sendmail(mail_from, mail_to, message.as_string())
        return True

    def __close(self):
        if self.__mail_server:
            self.__mail_server.close()

    def __enter__(self):
        self.__conn_server()
        if self.__mail_server:
            self._login(self.__username, self.__password)
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__close()


if __name__ == '__main__':
    m_from = "liuli6@dianrong.com"
    pwd = ""
    m_to = ["tan.zhang@dianrong.com"]
    msg = {
        "msg": "Test",
        "from": m_from,
        "subject": "Email Test"
    }
    with EmailSender(m_from, pwd) as m:
        ret = m.send_mail(m_from, m_to, msg)
        print(ret)
