"""rss_items 数据表"""
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "db.sqlite3")


def select_list_by_channel_link(link):
    """根据link来获取rss_item
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('select * from rss_items where channel_link=? order by pubDate desc', (link,))
    list = c.fetchall()
    conn.commit()
    conn.close()
    return list

def select_add_new_list ():
    """获取所有新生成的新闻"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('select * from rss_items where new_add=1')
    list = c.fetchall()
    conn.commit()
    conn.close()
    return list

def update_read_all():
    """全部标记已读"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('update rss_items set read = 1 where 1=1')
    conn.commit()
    conn.close()


def update_read_by_channel_link(channel_link):
    """根据 channel link 来标记已读"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('UPDATE rss_items SET read = 1 where channel_link=?', (channel_link,))
    conn.commit()
    conn.close()


def update_read_by_link(link):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('update rss_items set read = 1 where link=?', (link,))
    conn.commit()
    conn.close()


def update_all_rss(db_list):
    """
    更新所有订阅数据
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executemany('INSERT INTO rss_items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', db_list)
    conn.commit()
    conn.close()


def update_all_not_add_new():
    """设置所有新闻为不是新添加"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('update rss_items set new_add = 0')
    conn.commit()
    conn.close()


def delete_by_add_time(before_time):
    """删除时间线之前的新闻"""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE from rss_items where add_time', (before_time,))
    conn.commit()
    conn.close()


def get_link_keys():
    """
    获取所有link的list
    :return:
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('select link from rss_items where 1=1')
    list = c.fetchall()
    conn.commit()
    conn.close()
    return [item[0] for item in list]


if __name__ == '__main__':
    list = select_list_by_channel_link('https://www.infoq.cn/feed.xml')
    pass
