RSS_INFO = {
    'title': '少数派-最热',
    'link': 'https://sspai.com/api/v1/article/tag/page/get?limit=20&offset=0&tag=%E7%83%AD%E9%97%A8%E6%96%87%E7%AB%A0&released=false'
}


def run():
    import requests
    import demjson
    from core.CustomRss import CustomRss, CustomRssItem
    from datetime import datetime
    """少数派-最热"""
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
                item['summary'],
                item['summary'],
                datetime.fromtimestamp(item['released_time']).strftime('%Y-%m-%d %H:%M:%S'),
                item['id'],
                'https://sspai.com/post/%s' % item['id'],
                item['author']['nickname']
            ) for item in data['data']
        ]
    )
