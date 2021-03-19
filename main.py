import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QLineEdit, QLabel
import time
import requests
import re
from threading import Timer
# '在这里输入你的SendKey'
SendKey_def = -1
# '这里输入你的微博Cookie'
weibo_cookie = -1
# '在这里输入你的知乎Cookie'
zhihu_cookie = -1
if weibo_cookie == -1 or weibo_cookie == -1:
    print('请在main.py文件顶部完善Cookie')



def zhihu_top_spider():
    url = 'https://www.zhihu.com/hot'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': zhihu_cookie,
        # 'Authority': 'www.zhihu.com',
        # 'method':'GET',
        # 'Path': '/hot',
        # 'Scheme': 'https',
        # 'sec - fetch - dest': 'document',
        # 'sec - fetch - mode': 'navigate',
        # 'sec - fetch - site': 'none',
        # 'sec - fetch - user': '?1',
        'upgrade - insecure - requests': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    req.encoding = req.apparent_encoding
    html = req.text
    getTitle = re.compile('<h2 class="HotItem-title">(.*?)</h2>')
    getUrl = re.compile(r'<div class="HotItem-content"><a href="(.*?)" title')
    titleList = re.findall(getTitle, html)
    urlList = re.findall(getUrl, html)

    return titleList[:10], urlList[:10]


def baidu_top_spider():
    header = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}  # 伪装爬虫

    url = 'http://top.baidu.com/'
    req = requests.get(url, headers=header)
    req.encoding = req.apparent_encoding
    html = req.text
    getTitles = re.compile(r'<a target="_blank" title="(.*?)" data="1|1 href')
    getUrls = re.compile(r' class="list-title" href="(.*?)" href_top')
    titleList = re.findall(getTitles, html)
    urllist = re.findall(getUrls, html)

    return titleList[:10], urllist[:10]

def weibo_top_spider():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': weibo_cookie,
        'Host': 's.weibo.com',
        # 'Authority': 'www.zhihu.com',
        # 'method':'GET',
        # 'Path': '/hot',
        # 'Scheme': 'https',
        # 'sec - fetch - dest': 'document',
        # 'sec - fetch - mode': 'navigate',
        # 'sec - fetch - site': 'none',
        # 'sec - fetch - user': '?1',
        'upgrade - insecure - requests': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    pre_url = 'https://s.weibo.com'
    req = requests.get(url, headers=headers)
    req.encoding = req.apparent_encoding
    html = req.text
    getTitle = re.compile('target="_blank">(.*?)</a>')
    getUrl = re.compile(r'<a href="(.*?)" target')
    titleList = re.findall(getTitle, html)
    urlList = re.findall(getUrl, html)
    urlList_update = [pre_url+url for url in urlList]
    return titleList[:10], urlList_update[:10]

def auto_push(key, mode):
    mode_name = {
        'baidu': '百度头条',
        'zhihu': '知乎头条',
        'weibo': '微博头条'
    }
    time_cat = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + mode_name[mode]
    api = 'https://sc.ftqq.com/'
    api = api + key + '.send?'
    modeList = {
        'baidu':baidu_top_spider(),
        'zhihu':zhihu_top_spider(),
        'weibo':weibo_top_spider()
    }
    titleList, urlList = modeList[mode]
    desp = ''
    for title, url in zip(titleList, urlList):
        desp = desp + title + '  \n' + url + '  \n'
    data = {
        'text': time_cat,
        'desp': desp
    }
    req = requests.post(api, data)
    return req


def auto_push_repeat(key, hour):
    req1 = auto_push(key, 'baidu')
    req2 = auto_push(key, 'zhihu') 
    req3 = auto_push(key, 'weibo')
    if hour != 0:
        global timer
        timer = Timer(hour * 3600, auto_push_repeat, (key, hour))
        timer.start()




class work(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "网络头条自动推送系统"
        self.left = 300
        self.top = 300
        self.width = 400
        self.height = 500
        self.initUI()

    def initUI(self):

        # 主窗口
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        # 各按钮显示设计
        button_display_1 = QPushButton('全部推送', self)
        button_display_1.resize(100, 50)
        button_display_1.move(150, 300)
        button_display_2 = QPushButton('知乎头条推送', self)
        button_display_2.resize(100, 50)
        button_display_2.move(250, 400)
        button_display_3 = QPushButton('微博热榜推送', self)
        button_display_3.resize(100, 50)
        button_display_3.move(50, 400)
        button_display_4 = QPushButton('百度头条推送', self)
        button_display_4.resize(100, 50)
        button_display_4.move(150, 400)
        # self.lb_input = QLabel(self, text='状态')
        # self.lb_input.move(60, 250)
        # self.textbrowser = QTextBrowser(self)
        # self.textbrowser.resize(100,60)
        # self.textbrowser.move(150, 230)
        self.lb_input = QLabel(self, text='SCKEY')
        self.lb_input.move(180, 60)
        self.lb_input_2 = QLabel(self, text='间隔时间（小时）')
        self.lb_input_2.move(160, 160)
        self.te1 = QLineEdit(self)
        self.te1.move(50, 80)
        self.te1.resize(300, 30)
        self.te2 = QLineEdit(self)
        self.te2.move(50, 190)
        self.te2.resize(300, 30)
        button_display_4.clicked.connect(self.display_baidu)
        button_display_1.clicked.connect(self.display_auto)
        button_display_2.clicked.connect(self.display_zhihu)
        button_display_3.clicked.connect(self.display_weibo)

        # button_display.clicked.connect(self.display)
        # button_display_2.clicked.connect(self.display2)
        # button_display_3.clicked.connect(self.display3)
        # button_display_4.clicked.connect(self.display4)
    # 功能设计

    def display_baidu(self):
        try:
            SCKEY = self.te1.text() if self.te1.text() != '' else SendKey_def
            assert (SCKEY != '')
            req = auto_push(SCKEY, 'baidu')
        except:
            print('输入有误')


    def display_zhihu(self):
        try:
            SCKEY = self.te1.text() if self.te1.text() != '' else SendKey_def
            assert (SCKEY != '')
            req = auto_push(SCKEY, 'zhihu')
        except:
            print('输入有误')

    def display_weibo(self):
        try:
            SCKEY = self.te1.text() if self.te1.text() != '' else SendKey_def
            assert (SCKEY != '')
            req = auto_push(SCKEY, 'weibo')
        except:
            print('输入有误')

    def display_auto(self):
        try:
            SCKEY = self.te1.text() if self.te1.text() != '' else SendKey_def
            assert (SCKEY != '')
            hour = int(self.te2.text()) if self.te2.text() != '' else 0
            assert (isinstance(hour, int) or isinstance(hour, float))
            req = auto_push_repeat(SCKEY, hour)
        except:
            print('输入有误')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = work()
    ex.show()
    sys.exit(app.exec_())
