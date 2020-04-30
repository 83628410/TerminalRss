"""定时任务"""
import terminal


def start():
    # 发送任务
    terminal.exec_send_mail()


if __name__ == '__main__':
    start()
