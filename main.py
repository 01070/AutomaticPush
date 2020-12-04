import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QLineEdit, QLabel
import time
import requests
import re
from threading import Timer


def zhihu_top_spider():
    url = 'https://www.zhihu.com/hot'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie':'_zap=411babfc-e770-465d-b7b9-52bffc363e0b; d_c0="AFCl2apQlRCPTjYea_vwVbIsuEsSzCwgVT4=|1577678274"; _xsrf=wVSeGxps1Mr2isWB66HrocZX6URQBVsF; __utmz=51854390.1578986731.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _ga=GA1.2.1360518270.1578986731; tst=h; tshl=; r_cap_id="Mzk2ZjZkNWI4NzU5NDRmNWI4MDAzNDdhZWY0ZTQ5ZmY=|1605663975|2f22e0b5b7886a8e7ad4888b95cee02fdf92c7d4"; cap_id="NTY2Nzc1NTc4ZjQzNDE1OThhYTEyNjAwMTQzYjE0OTE=|1605663975|b1b41fbfa0bf01a1fb9b19cd5798d89c80bc5e71"; l_cap_id="MDMwNmVkNzk2NWE5NGUwMDk5YmU0YzhjZjRhNmZjMTY=|1605663975|19bb84461c542a94d4680d2a6d85fac236eda92c"; auth_type=d2VjaGF0|1605663988|5e27b05698d15fdd7635fe17372ac5a45e821182; token="MzlfOG05cDJ5eFNYOEItWExzYzEyNE1fLTlhalRmOUZNYlViZ0J0NVpFQ0lRZXFpNHlHYUdHQmtiVnZZRXZ4R0ZGR0d1R1FZcnRjd2dsVy1JM2FJUGxKMmR4SjlVMTh0aVpmYnRhaXNwWTU1RGs=|1605663988|0b463576fd78ec808adb49427335ed997666c3f8"; client_id="bzNwMi1qalRYTzVleHFybnl6MXNia3Y4eE5TRQ==|1605663988|7c160c43891153984832b917c6f4b0d987030a6f"; capsion_ticket="2|1:0|10:1605664010|14:capsion_ticket|44:OWYwMmJmMDJlZTNiNDVhMWE4OTdkOGE5ZDEwMzgwOWE=|cf30d172ad6cc7007c71005abe6d3a0578f24a7cbdee57c04424113022ab2d45"; z_c0="2|1:0|10:1605664010|4:z_c0|92:Mi4xM3dSNkFBQUFBQUFBVUtYWnFsQ1ZFQ1lBQUFCZ0FsVk5Dc3VoWUFDaDU4dVZOcG1EcVZXanJ3eXJZcS1vNVVkUWJn|f917ca7c073c036e10e76bf2a99493ff49dc4b2a352005a27aece3a7afb64a0e"; __utmv=51854390.100-1|2=registration_date=20140908=1^3=entry_date=20140908=1; __utma=51854390.1360518270.1578986731.1606379460.1606464431.15; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1606909001,1606969367,1606996215,1606997480; q_c1=1bfa41cae2d040b7a8d6dfd02376f258|1606997513000|1578986733000; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1607041079; SESSIONID=MMZ1yQlaXOQDOBQQ5em6ILYs40u1r1hHHaQwXsurFtu; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1607041113|1607041067; JOID=VVwSC0s7Hanht_a9ODRZ-0m4bjYpdVP82Mmk0lZkUfuq8LPvamKRZ7Gz9rE_Mm0789kzH5y2Qksytqk4WJ-MF2g=; osd=VVgWBUw7Ga3vsPa5PDpe-028YDEpcVfy38mg1lhjUf-u_rTvbmafYLG38r84Mmk__d4zG5i4RUs2sqc_WJuIGW8=',
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
        'Cookie': 'SINAGLOBAL=9427721340678.658.1577837894348; SSOLoginState=1606877212; _s_tentry=login.sina.com.cn; Apache=4679169351629.784.1606877183479; ULV=1606877183484:125:2:3:4679169351629.784.1606877183479:1606805101522; SCF=AipCrdtDVs0DMqiAcDCIu5DlVqhgUBPQvBEJaBBCPMkj7Iiju_Up6h_RuNsizyYJ8Nn9vUau4asYyR0YiUiymUQ.; SUB=_2A25yzfh-DeRhGeBN6VYY8CjNzjuIHXVRu262rDV8PUJbmtAfLVGgkW9NRJG5hwU2chxpZfciRT2Sgjtll-2XD2P6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh.TQ2B19Sr2bKsk3uqncwL5JpX5K-hUgL.Foq0eoB4ehqpSKM2dJLoIEXLxKML12-L12zLxKMLBKML1h5LxK.LBo.L1h-LxKqL1-eLB-eLxK.LBo.L1h-t; ALF=1638579116; wvr=6; UOR=,,login.sina.com.cn; webim_unReadCount=%7B%22time%22%3A1607043089459%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A4%2C%22msgbox%22%3A0%7D; WBStorage=8daec78e6a891122|undefined',
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
    # print('can do')

def auto_push_repeat(key, hour):
    req1 = auto_push(key, 'baidu')
    req2 = auto_push(key, 'zhihu') 
    req3 = auto_push(key, 'weibo')
    global timer
    timer = Timer(int(hour) * 3600, auto_push_repeat, (key, hour))
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
        button_display_1 = QPushButton('自动推送', self)
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
        SCKEY = self.te1.text() if self.te1.text() != '' else 'SCU131854Tb2f53e60051aa5f75deaff33121df6635fc6e4e36f6fa'
        req = auto_push(SCKEY, 'baidu')

    def display_zhihu(self):
        SCKEY = self.te1.text() if self.te1.text() != '' else 'SCU131854Tb2f53e60051aa5f75deaff33121df6635fc6e4e36f6fa'
        req = auto_push(SCKEY, 'zhihu')

    def display_weibo(self):
        SCKEY = self.te1.text() if self.te1.text() != '' else 'SCU131854Tb2f53e60051aa5f75deaff33121df6635fc6e4e36f6fa'
        req = auto_push(SCKEY, 'weibo')

    def display_auto(self):
        SCKEY = self.te1.text() if self.te1.text() != '' else 'SCU131854Tb2f53e60051aa5f75deaff33121df6635fc6e4e36f6fa'
        hour = self.te2.text() if self.te2.text() != '' else '3'
        req = auto_push_repeat(SCKEY, hour)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = work()
    ex.show()
    sys.exit(app.exec_())