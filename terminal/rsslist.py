import math
import os
import re

import terminal
from config import RSS_CONFIG
from core.rss import get_site_rss_channel_title_link_dict
from db import rss_items
from prompt_toolkit import print_formatted_text, HTML, prompt
from prompt_toolkit.formatted_text import FormattedText
from terminal import terminal_config


def bottom_toolbar_page(total_page, pageNo):
    return [
        ('class:bottom-toolbar', '[ b ]返回  [ r ]设置频道为已读  [ n ]下一页  [ p ]上一页 '),
        ('class:bottom-toolbar-bold', '[ ' + str(pageNo) + '/' + str(total_page) + ' ]')
    ]


def _get_list_by_page(rss_items_list, page, page_size):
    """分页显示list"""
    rss_id = 0
    message = []
    has_more = True

    total_page = math.ceil(len(rss_items_list) / page_size)

    start_index = (page - 1) * page_size
    end_index = page * page_size

    if end_index >= len(rss_items_list):
        end_index = len(rss_items_list)
        has_more = False

    for item in rss_items_list[start_index: end_index]:
        message.append(('class:index', '[ ' + str(rss_id) + ' ] '))
        message.append(('', '  '))
        if item[10] == 0:
            message.append(('class:title', item[3]))
        else:
            message.append(('class:read', item[3]))
        message.append(('', '  '))
        message.append(('class:time', item[6]))
        message.append(('', '\r\n'))
        rss_id = rss_id + 1

    return message, has_more, total_page, rss_items_list[start_index: end_index]


def exec_command_open_browse(url):
    """浏览器打开网址"""
    rss_items.update_read_by_link(url)
    os.system('open ' + url)


def exec_news_list(name, url):
    """加载rss url的信息"""
    rss_items_list = rss_items.select_list_by_channel_link(url)

    current_page = 1

    terminal_config.PROMPT_MESSAGE_BASE.append(('', name))
    terminal_config.PROMPT_MESSAGE_BASE.append(('class:path', '>'))

    def bottom_toolbar():
        return [
            ('class:bottom-toolbar', '[ b ]返回'),
            ('class:bottom-toolbar', '  [ r ]设置频道为已读'),
        ]

    while True:
        msg, has_more, total_page, rss_list = _get_list_by_page(rss_items_list, current_page, 20)

        print_formatted_text(FormattedText(msg), style=terminal_config.STYLE)

        num = -1

        try:
            if current_page < total_page:
                user_input = prompt(terminal_config.PROMPT_MESSAGE_BASE, style=terminal_config.STYLE,
                                    bottom_toolbar=bottom_toolbar_page(total_page, current_page))
            else:
                user_input = prompt(terminal_config.PROMPT_MESSAGE_BASE, style=terminal_config.STYLE,
                                    bottom_toolbar=bottom_toolbar)

            num = int(user_input)

        except KeyboardInterrupt:
            print('bye bye !!!')
            exit()
            break
        except EOFError:
            print('bye bye !!!')
            exit()
            break
        except ValueError:
            pass

        if user_input == 'b':
            terminal_config.PROMPT_MESSAGE_BASE = terminal_config.PROMPT_MESSAGE_BASE[0:-2]
            break

        elif user_input == 'n' and has_more is True:
            current_page += 1
            continue

        elif user_input == 'p' and current_page != 1:
            current_page -= 1
            continue

        elif user_input == 'r':
            rss_items.update_read_by_channel_link(url)
            print('已将频道[' + name + ' ] 全部文章标记为已读')
            continue

        elif 0 <= num < len(msg):
            exec_command_open_browse(rss_list[int(user_input)][8])
            continue


def exec_channel_list():
    """加载所有频道列表"""
    name_list = RSS_CONFIG['RSS_URL_LIST']

    name_list.update(get_site_rss_channel_title_link_dict())

    nl = []
    num = 0
    for k, v in name_list.items():
        nl.append('[ ' + str(num) + ' ] ' + '<b>' + k + '</b>')
        num += 1


    name_keys = [item for item in name_list.keys()]

    terminal_config.PROMPT_MESSAGE_BASE.append(('', 'channel'))
    terminal_config.PROMPT_MESSAGE_BASE.append(('class:path', '>'))

    def bottom_toolbar():
        return [
            ('class:bottom-toolbar', '[ b ]返回'),
            ('class:bottom-toolbar', '  [ r + 编号 ]设置频道为已读'),
        ]

    while True:
        print_formatted_text(HTML("\r\n".join(nl)))

        num = -1
        try:
            user_input = prompt(terminal_config.PROMPT_MESSAGE_BASE, style=terminal_config.STYLE,
                                bottom_toolbar=bottom_toolbar)
            num = int(user_input)
        except KeyboardInterrupt:
            print('bye bye !!!')
            exit()
            break
        except EOFError:
            print('bye bye !!!')
            exit()
            break
        except ValueError:
            pass

        if user_input == 'b':
            terminal_config.PROMPT_MESSAGE_BASE = terminal_config.PROMPT_MESSAGE_BASE[0:-2]
            break
        if num >= 0:
            name = name_keys[int(user_input)]
            url = name_list[name]
            exec_news_list(name, url)
            continue
        if re.match(r'r \d+', user_input) is not None:
            channel_name = name_keys[int(re.findall(r'\d+', user_input)[0])]
            channel_link = name_list[channel_name]
            terminal.exec_read_by_channel(channel_link)
            print('频道：', channel_name, '设置为已读成功')
            continue
