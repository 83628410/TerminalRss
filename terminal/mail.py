"""发送邮件"""

import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText

from config import RSS_MAIL_CONFIG
from db import rss_items


def exec_send_mail():
    """开始发送"""
    print('开始发送邮件')
    # 获取所有数据库新增的新闻
    news_list = rss_items.select_add_new_list()
    if len(news_list) == 0:
        return
    mail_msg = '<h1>terminal-rss</h1>'
    for item in news_list:
        pubDate = time.strptime(item[6], "%Y-%m-%d %H:%M:%S")
        mail_msg += '<p><a href="%s"><span style="color:#660000;">%s</span>  %s  <span style="color:#cccccc;">%s</span></a></p>' % (
            item[8], item[0], item[3], time.strftime("%Y-%m-%d %H:%M", pubDate))

    try:
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = Header("terminal-rss", 'utf-8')
        message['To'] = Header('terminal-rss user', 'utf-8')
        message['Subject'] = Header('terminal-rss ' + time.strftime("%Y-%m-%d %H:%M", time.localtime()), 'utf-8')
        smtp_obj = smtplib.SMTP_SSL(RSS_MAIL_CONFIG['HOST'], 465)
        smtp_obj.login(RSS_MAIL_CONFIG['SENDER'], RSS_MAIL_CONFIG['PWD'])
        smtp_obj.sendmail(RSS_MAIL_CONFIG['SENDER'], RSS_MAIL_CONFIG['RSS_RECEIVERS'], message.as_string())
        smtp_obj.quit()

        print('邮件发送成功')
        rss_items.update_all_not_add_new()
    except smtplib.SMTPException as e:
        print('邮件发送失败', e)

