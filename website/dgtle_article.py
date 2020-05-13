RSS_INFO = {
    'title': '数字尾巴-文章-最新',
    'link': 'https://www.dgtle.com/article/getList/0?page=1&pushed=0&last_id=0'
}


def run():
    import requests
    import demjson
    from core.CustomRss import CustomRss, CustomRssItem
    from datetime import datetime
    """数字尾巴-文章-最新"""

    r = requests.get(RSS_INFO['link'], timeout=10000)

    r.encoding = 'utf-8'
    data = demjson.decode(r.text)

    itemList = data['data']['dataList']

    return CustomRss(
        RSS_INFO['title'],
        RSS_INFO['link'],
        RSS_INFO['title'],
        [
            CustomRssItem(
                item['title'],
                item['content'],
                item['content'],
                datetime.fromtimestamp( int(item['created_at']) ).strftime('%Y-%m-%d %H:%M:%S'),

                item['id'],
                'https://www.dgtle.com/article-%s-1.html' % item['id'],
                item['user_name']
            ) for item in itemList
        ]
    )
