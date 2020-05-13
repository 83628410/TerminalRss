RSS_INFO = {
    'title': 'V2EX-追热主题',
    'link': 'https://www.v2ex.com/api/topics/hot.json'
}


def run():
    import requests
    import demjson
    from core.CustomRss import CustomRss, CustomRssItem
    from datetime import datetime
    """获取远程数据 v2ex热榜"""
    r = requests.get(RSS_INFO['link'], timeout=10000)
    r.encoding = 'utf-8'
    data = demjson.decode(r.text)
    return CustomRss(
        RSS_INFO['title'],
        RSS_INFO['link'],
        RSS_INFO['title'],
        [
            CustomRssItem(
                item['title'],
                item['content_rendered'],
                item['content'],
                datetime.fromtimestamp(item['created']).strftime('%Y-%m-%d %H:%M:%S'),
                item['id'],
                item['url'],
                item['member']['username']
            ) for item in data
        ]
    )
