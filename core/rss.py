"""rss 通用的解析支持"""
import fnmatch
import os
import sys
import time
from typing import Dict, Any

import feedparser
from config import RSS_CONFIG
from .CustomRss import CustomRss, CustomRssItem


def get_custom_rss(title, link, description):
    rss = feedparser.parse(link)
    return CustomRss(
        title,
        link,
        description,
        [CustomRssItem(
            item.get('title'),
            item.get('summary'),
            item.get('summary'),
            time.strftime("%Y-%m-%d %H:%M:%S", item.get('published_parsed')),
            0,
            item.get('link'),
            item.get('author')
        ) for item in rss.entries]
    )


def get_all_rss_db(link_list):
    """获取所有rss 信息插入数据库使用"""

    # 获取自定已定义的rss 列表
    custom_rss_list = load_site_rss_all()
    # 获取普通的rss列表
    rss_list = RSS_CONFIG['RSS_URL_LIST']

    # 正规rss 数据
    for k, v in rss_list.items():
        custom_rss = get_custom_rss(k, v, k)
        db_list = []
        for item in custom_rss:
            if item.link not in link_list:
                db_list.append(
                    (
                        k,
                        v,
                        k,
                        item.title,
                        item.description,
                        item.content,
                        item.pubDate,
                        item.guid,
                        item.link,
                        item.author,
                        0,
                        1,
                          time.time()
                    )
                )
        yield db_list
    #    自定义网址转成rss 格式
    for file_name in custom_rss_list:
        custom_rss_obj = custom_rss_list[file_name]['run']()
        db_list = []
        for item in custom_rss_obj:
            if item.link not in link_list:
                db_list.append(
                    (
                        custom_rss_obj.title,
                        custom_rss_obj.link,
                        custom_rss_obj.description,
                        item.title,
                        item.description,
                        item.content,
                        item.pubDate,
                        item.guid,
                        item.link,
                        item.author,
                        0,
                        1,
                        time.time()
                    )
                )
        yield db_list


def count_all_rss():
    """获取所有rss 数量"""
    # 获取自定已定义的rss 列表
    custom_rss_list = load_site_rss_all()
    # 获取普通的rss列表
    rss_list = RSS_CONFIG['RSS_URL_LIST']

    return len(custom_rss_list) + len(rss_list)


def get_site_rss_channel_title_link_dict():
    """获取所有 site rss 的 title link dict
    :return Dict { '频道title' :'频道link'}
    """
    result: Dict[str, str] = {}
    rss_list = load_site_rss_all()
    for n, v in rss_list.items():
        result[v['title']] = v['link']

    return result


def load_site_rss_all():
    """加载所有site 包下的py文件"""

    result: Dict[str, Dict[str, Any]] = {}

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "../website")

    for root, dirs, files in os.walk(db_path):
        for site_item in files:
            if site_item is None or '__init__.py' == site_item:
                continue

            if not fnmatch.fnmatch(site_item, '*.py'):
                continue
            py_name = 'website.' + site_item.replace('.py', '')

            __import__(py_name)

            if hasattr(sys.modules[py_name], 'run') and hasattr(sys.modules[py_name], 'RSS_INFO'):
                result[py_name] = {
                    'title': sys.modules[py_name].RSS_INFO['title'],
                    'link': sys.modules[py_name].RSS_INFO['link'],
                    'run': sys.modules[py_name].run
                }
            else:
                raise Exception('function not found ')

    return result
