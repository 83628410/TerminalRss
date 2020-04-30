"""命令行中的样式"""
from prompt_toolkit.styles import Style

STYLE = Style.from_dict({
    '': '',
    'index': '#884444',
    'time': '#cccccc ansicyan',
    'title': 'bold',
    'at': '#00aa00',
    'colon': '#0000aa',
    'pound': '#00aa00',
    'host': '#00ffff bg:#444400',
    'path': '#00aa00 ansicyan',
    'bottom-toolbar': '#ffffff bg:#CC0000',
    'bottom-toolbar-bold': '#ffffff bg:#CC0000 bold',
    'read': '#666666'
})

PROMPT_MESSAGE_BASE = [
    ('', 'cj-rss'),
    ('class:path', '>'),
]
