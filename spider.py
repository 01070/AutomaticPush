import requests
from bs4 import BeautifulSoup
def baidu_top_spider(number=8):
    header = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}  # 伪装爬虫

    url = 'http://top.baidu.com/'
    req = requests.get(url, headers=header)
    req.encoding = req.apparent_encoding
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    title = []
    for x in bs.find_all('a', class_='list-title'):
        title.append(x.get_text())
    return title[:number]


def zhihu_top_spider(number=8):
    url = 'https://www.zhihu.com/billboard'
    header = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}#伪装爬虫
    req = requests.get(url, headers=header)
    req.encoding = req.apparent_encoding
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    title = []
    for x in bs.find_all('div', class_='HotList-itemTitle'):
        title.append(x.get_text())
    return title[:number]


def weibo_top_spider(number=8):
    url = 'https://s.weibo.com/top/summary?Refer=top_hot&topnav=1&wvr=6'
    header = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}#伪装爬虫
    req = requests.get(url, headers=header)
    req.encoding = req.apparent_encoding
    html = req.text
    bs = BeautifulSoup(html, 'lxml')
    title = []
    content = bs.find('div', class_='data')
    for x in content.find_all('a'):
        title.append(x.get_text())
    return title[:number]

