#!/usr/bin/env python
import terminal
from prompt_toolkit import PromptSession
from terminal import terminal_config

def bottom_toolbar():
    return [('class:bottom-toolbar', ' [ l ]rss 频道列表  [ e ]退出  [ u ]更新数据库 [ r ]设为全部已读 [ s ]发送邮件')]


if __name__ == '__main__':

    session = PromptSession()
    while True:
        try:
            answer = session.prompt(terminal_config.PROMPT_MESSAGE_BASE, style=terminal.STYLE,
                                    bottom_toolbar=bottom_toolbar)
        except KeyboardInterrupt:
            break
        except EOFError:
            break
        if answer == 'l':
            terminal.exec_channel_list()
            continue
        if answer == 'u':
            terminal.exec_update_all()
            continue
        if answer == 'r':
            terminal.exec_read_all()
            print('设置所有新闻为已读成功')
            continue
        if answer == 's':
            terminal.exec_send_mail()
            continue
        if answer == 'e':
            break

    print("bye bye !!")
