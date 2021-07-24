# AutomaticPush  
自动爬取知乎 微博 百度头条，通过server酱推送到微信
## requirement  
* PyQt5
* torch>=1.0
## 使用方法  
1. 获取SendKey,在[这里](https://sct.ftqq.com/sendkey) 绑定微信账号  
2. 在run.py文件中完善Cookie信息。  
3. python run.py  
4. 在第一次使用时，需要输入SendKey码，之后系统会将SendKey码保存到本地文件中，无需再次输入，当重新输入时，系统也会修改本地的文件。在间隔时间处可填写推送的间隔，从而实现定时的推送（可空缺，此时系统会默认24小时推送一次）  
5. 选择推送内容

![image][]



