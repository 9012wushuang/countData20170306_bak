#!/usr/local/bin/python3
# coding:utf-8


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_mail():
    host = 'smtp.exmail.qq.com'
    port = 25  # 25 为 SMTP 端口号
    sender = ''  # todo 发件人
    receivers = []  # todo 接收邮件，可设置为你的QQ邮箱或者其他邮箱 格式：'邮箱1'，'邮箱2'
    mail_user = ''  # todo 邮箱名
    mail_pass = ''  # todo 邮箱密码

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("saas", 'utf-8')
    message['To'] = Header("saas", 'utf-8')
    subject = 'saas 数据监控'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('附件为数据统计文件', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('', 'rb').read(), 'base64', 'utf-8')  # todo 添加附件
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="saasCountData.csv"'  # todo  添加显示名称(暂以英文展示)
    message.attach(att1)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(host, port)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# print(send_mail())
