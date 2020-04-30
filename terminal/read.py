"""标记为已读"""
import db.rss_items as rss_items

def exec_read_all():
    """标记全部新闻为已读"""
    rss_items.update_read_all()

def exec_read_by_channel(channel_link):
    """标记某个频道为已读"""
    rss_items.update_read_by_channel_link(channel_link)

def exec_read_by_link(link):
    """标记某个链接为已读"""
    rss_items.update_read_by_link(link)