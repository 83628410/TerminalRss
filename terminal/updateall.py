import time

from core.rss import get_all_rss_db, count_all_rss
from db import rss_items
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import ProgressBar


def exec_update_all():
    """
    更新全部rss 内容到数据库
    :return:
    """
    amount_rss = count_all_rss()
    # 已经加入的rss item link 列表
    already_link_list = rss_items.get_link_keys()
    # 标记所有新闻为不是最新
    rss_items.update_all_not_add_new()
    # 获取所有信息
    g = get_all_rss_db(already_link_list)

    list = []

    title = HTML('<style bg="yellow" fg="black">加载RSS最新内容</style>')
    label = HTML('<ansired>加载RSS最新内容</ansired>: ')

    with ProgressBar(title=title) as pb:
        for i in pb(range(amount_rss), label=label):
            time.sleep(.01)
            try:
                result = next(g)
                list.extend(result)
            except StopIteration:
                pass


    if len(list) == 0:
        print('没有新的内容')
    else:
        print('保存到数据库...')
        rss_items.update_all_rss(list)
        print('保存数据库成功，', '共保存：' + str(len(list)))
