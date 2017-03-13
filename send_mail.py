#!/usr/local/bin/python3
# coding:utf-8


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def send_mail():
    host = 'smtp.exmail.qq.com'
    port = 25  # 25 为 SMTP 端口号
    sender = 'bifenghui@edianzu.cn'
    receivers = ['1641909357@qq.com', 'wangqing@edianzu.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    mail_user = 'bifenghui@edianzu.cn'
    mail_pass = 'asnMM5396362'

    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("saas", 'utf-8')
    message['To'] = Header("saas", 'utf-8')
    subject = 'saas 数据监控'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文内容
    message.attach(MIMEText('附件为数据统计文件', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open('bifenghui.csv', 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="saasCountData.csv"'
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
