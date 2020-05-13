"""定时任务"""
import terminal


def start():
    # 更新全部内容到数据库
    terminal.updateall()
    # 发送任务
    terminal.exec_send_mail()


if __name__ == '__main__':
    start()
