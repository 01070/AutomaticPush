import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,\
    QLineEdit, QLabel
import time
import requests
import re
from threading import Timer
from bs4 import BeautifulSoup
from utils import predict_run4push

def zhihu_top_spider():
    url = 'https://www.zhihu.com/hot'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie':'_zap=411babfc-e770-465d-b7b9-52bffc363e0b; d_c0="ACl2apQlRCPTsjYea_vwVbIsuEsSzCwgVT4=|1577678274"; _xsrf=wVSeGxps1Mr2isWB66HrocZX6URQBVsF; _ga=GA1.2.1360518270.1578986731; __snaker__id=v5ifdofM1mvp3OvV; _9755xjdesxxd_=32; YD00517437729195%3AWM_TID=AsFC%2FPZBCG1AQRBUBUMuxra6q%2FdcNa72; q_c1=1bfa41cae2d040b7a8d6dfd02376f258|1622960582000|1578986733000; __utma=51854390.1360518270.1578986731.1606464431.1622960582.16; __utmz=51854390.1622960582.16.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|2=registration_date=20140908=1^3=entry_date=20200114=1; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1626311893; captcha_session_v2="2|1:0|10:1626311895|18:captcha_session_v2|88:bXhZNDJtL09ySSthdVp6ekh5T1haeWMyd2Q0YkE4Mk1UYUNRalgrdzhLOTV3cG4rMm1uRXVNbFNrbkE4RU5lcA==|a954766337cb4dd4b69241c2d4be653e230b097b7e4ca0790f882ae63cf88b5e"; SESSIONID=LxrtPPcB3r4q2rCQNg6FqEDS2TajlTKdUUdeaFZsnlJ; JOID=UlwVCkubf07VfDQzXJI7HHx0qrhN0wM1qCxgVBeoCX6tR0Z0CUP-obx4ND5cOUEfiNGwXE9Ud2TDRp2LmPsmRvU=; osd=UlgWB0ybe03YezQ3X588HHh3p79N1wA4ryxkVxqvCXquSkF0DUDzprx8NzNbOUUchdawWExZcGTHRZCMmP8lS_I=; gdxidpyhxdE=o6H5BzX4DuYKPiwvJzfdx0YUQbfbIUQJr4HBT1Jbs0gE6CiCdTcExplNOgbyuaOnwj93phRuJU9ww%2F%2FTbOmGS9j%2F%5C%2BpXvOZDOM1WG4Uuait%2BT60bUUkUToYqojZBo%2F%2BOka4PMsCcSUn8zT%5CAA0z%2FVS67%5CbKfw4qaLGvvfb2%5C%2FiqKbLsw%3A1626312794283; YD00517437729195%3AWM_NI=MIxQ4MUs4Zfo2EX%2B4nYcRVDBze%2Bldj9X%2Bg7oiZCvJZkRqQcyMzRb0i0Du3NJrPHJqEjgEajponSSiq1S0IsUBx4Csq0ORAmP610uyS8IWp5I094WcIRZ97uxTjDCj4kseHk%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6ee8ab16087b4fdaee763f8a88ab2c54b979b8f85f8628bb8bf8baa6d9baa8789f42af0fea7c3b92a8f97b8b2b74797adfcbbe565f29b98ccb7669bbd9eb7c74ababbe58de762fb88e588b665ab868d97c952a98ebfb2e2738fa69e83b363f49cbbd4cd42b29088abf44faab98b82e97cadb29db4ec7bf38d00aaf25f82a8fca4f27bf4919ea2f05cf6ef0096fc59fc979991b843f4e7fcb8e2439286f7d8f87498b68ca4e940a9adaba9ea37e2a3; captcha_ticket_v2="2|1:0|10:1626311906|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfUkpTU0t2V3pYakg0OExDRUFTd0d3VjI4ZnhjaDhwc3dPVENSNjE2OFQyeC4wZVZVT202VzRPNVUyaEZ0RUk3VWJsSElTOGFkVEFWOHJWR2pBclItYWRqbjc0Q2JkeDFOZlpZY2JxUVo2QVdfVmZiU1BoTmFwTmRxLXVVTGEuZ1NiUzlHYnQyWFptczU0RVNlV2ZiOGFYQlJkQUlPdXAtclN0LlZ1Qy1mTk91WXJCdDFta0pDMGtRWktZeGdpQndKZmpBLV9BNS1QNlBmNnJvQi1iMEVsSkh6OWhUSi12RnBFZGlOdl9tVG1pQ1dxSklIbTBmS0Jsd3dGay1sZmJqeHFRLkZaN0ZkbV9ka3VoNC5hX3BPNC4wUUguWnluQi5iNVU1cDBkZ1FSRk5kd0pzcWIuOXg0cHgtVjRVX0lTZVh6dFdrVWdpVnNhUFR3LXRockNOdi5YRmZSRzEyZnlULnVDbXpJSzBsY1MyaVlsbXktRDRhV3ZIZ2FwOGRhQzRvSi5TR05ZSlhodk5ZZExVLU9UYkRqLTdQaHlIV1UxckNlLnBzYUtFcFJtSkRYNzVwbEd3OGN3Q1B4WDV4azdZTFNzVWhFel9wLXQ2T0RNWHhoTmVMVExTQTV5WkNLZWV5ZnBmRWlCcWtwNERwbl82RG5fNUZURS1IX29GMyJ9|48648fda288d81631bf87f771c7bac6a85abfa09833c96ead18aca841cb8d997"; z_c0="2|1:0|10:1626311906|4:z_c0|92:Mi4xM3dSNkFBQUFBQUFBVUtYWnFsQ1ZFQ1lBQUFCZ0FsVk40dHJjWVFBbUd5ZEdiS202eEJaYTJEOEtfdmRVYWJrRFpR|836a516818d6bb1718ce62da42e59bde1a7f5543cd8cc90c32e5987e01a2c677"; tshl=; tst=h; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1626311905; KLBRSID=9d75f80756f65c61b0a50d80b4ca9b13|1626311907|1626311895',
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
    titleList_ = predict_run4push(titleList[:10])

    return titleList_, urlList[:10]


def baidu_top_spider():
    urllist_ = []
    header = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}  # 伪装爬虫

    url = 'http://top.baidu.com/'
    req = requests.get(url, headers=header)
    req.encoding = req.apparent_encoding
    html = req.text
    soup = BeautifulSoup(html)
    # getTitles = re.compile(r'class="c-single-text-ellipsis>"(.*?)</div>')
    getUrls1 = re.compile(r'class="item-wrap_2oCLZ active"(.*?)" target="_blank">')
    getUrls2 = re.compile(r'class="item-wrap_2oCLZ "(.*?)" target="_blank">')
    titleContent = soup.find_all(name='div', class_='c-single-text-ellipsis')
    tileList = [title.string for title in titleContent]

    # titleList = re.findall(getTitles, html)
    titleList_ = predict_run4push(tileList[:-3:2])
    urllist = re.findall(getUrls1, html)
    urllist_.append(re.sub('href="', '', urllist[0]))
    urllist2 = re.findall(getUrls2, html)
    for url in urllist2:
        urllist_.append(re.sub('href="', '', url))
    return titleList_, urllist_[:10]

def weibo_top_spider():
    url = 'https://s.weibo.com/top/summary?cate=realtimehot'
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'SINAGLOBAL=1493116408036.9385.1616917718110; SUBP=0033WfrSXqPxfM725Ws9jqgMF5529P9D9Wh.TQ2B19Sr2bKsk3uqncwL5JpX5K-hUgL.Foq0eoB4ehqpSKM2dJLoIEXLxKML12-L12zLxKMLBKML1h5LxK.LBo.L1h-LxKqL1-eLB-eLxK.LBo.L1h-t; wvr=6; UOR=,,login.sina.com.cn; SCF=As41YUbARfCs0yEmw9wKUxQ1pf4kNO7ZI7xuSVZJ8GQntL6RONTZxFbzCR6yWizd-UKv2KgJ0pi_9V84nUx7m-w.; SUB=_2A25N_smMDeRhGeBN6VYY8CjNzjuIHXVujbxErDV8PUJbmtB-LUOgkW9NRJG5h18eScBhVRGI6ScdM-3ou3UqBoUg; ALF=1658580315; SSOLoginState=1627044316; _s_tentry=login.sina.com.cn; Apache=7408768118597.193.1627044318452; ULV=1627044318561:5:2:2:7408768118597.193.1627044318452:1626831233759; webim_unReadCount=%7B%22time%22%3A1627044321175%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D; WBStorage=2ceabba76d81138d|undefined',
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
    titleList_ = predict_run4push(titleList[:10])
    return titleList_, urlList_update[:10]

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
        'baidu':baidu_top_spider,
        'zhihu':zhihu_top_spider,
        'weibo':weibo_top_spider
    }
    titleList, urlList = modeList[mode]()
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
        if self.te1.text() != '':
            SCKEY = self.te1.text()
        elif os.path.isfile('SCKEY.val'):
            with open('SCKEY.val', 'r') as f:
                SCKEY = f.readline()
        else:
            SCKEY = ''

        assert SCKEY != '', 'SCKEY is none! please type your SCKEY'





        with open('SCKEY.val', 'w') as f:
            f.write(SCKEY)


        req = auto_push(SCKEY, 'baidu')

    def display_zhihu(self):

        if self.te1.text() != '':
            SCKEY = self.te1.text()
        elif os.path.isfile('SCKEY.val'):
            with open('SCKEY.val', 'r') as f:
                SCKEY = f.readline()
        else:
            SCKEY = ''

        assert SCKEY != '', 'SCKEY is none! please type your SCKEY'





        with open('SCKEY.val', 'w') as f:
            f.write(SCKEY)

        req = auto_push(SCKEY, 'zhihu')

    def display_weibo(self):

        if self.te1.text() != '':
            SCKEY = self.te1.text()
        elif os.path.isfile('SCKEY.val'):
            with open('SCKEY.val', 'r') as f:
                SCKEY = f.readline()
        else:
            SCKEY = ''

        assert SCKEY != '', 'SCKEY is none! please type your SCKEY'




        with open('SCKEY.val', 'w') as f:
            f.write(SCKEY)

        req = auto_push(SCKEY, 'weibo')

    def display_auto(self):
        if self.te1.text() != '':
            SCKEY = self.te1.text()
        elif os.path.isfile('SCKEY.val'):
            with open('SCKEY.val', 'r') as f:
                SCKEY = f.readline()
        else:
            SCKEY = ''

        assert SCKEY != '', 'SCKEY is none! please type your SCKEY'
        hour = self.te2.text() if self.te2.text() != '' else '3'
        req = auto_push_repeat(SCKEY, hour)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = work()
    ex.show()
    sys.exit(app.exec_())
