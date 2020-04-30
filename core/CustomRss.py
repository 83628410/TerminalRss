"""rss 格式"""


class CustomRss:
    def __init__(self, title, link, description, items) -> None:
        self.title = title
        self.link = link
        self.description = description
        self.items = items

        self._item_index = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self._item_index >= len(self.items)-1:
            raise StopIteration
        self._item_index += 1
        return self.items[self._item_index]


class CustomRssItem:
    def __init__(self, title, description, content, pubDate, guid, link, author) -> None:
        self.title = title
        self.description = description
        self.content = content
        self.pubDate = pubDate
        self.guid = guid
        self.link = link
        self.author = author
