# # card1 = "1001"
# # pwd1 = "123456"
# # ban1 = 10000
# #
# # card2 = "1002"
# # pwd2 = "123456"
# # ban2 = 10000
# #
# # card3 = "1003"
# # pwd3 = "123456"
# # ban3 = 10000
# #
# # print("欢迎来到中国银行")
# # times = 0
# # while True:
# #     card = input("请输入银行卡号:")
# #     pwd = input("请输入密码:")
# #
# #     ban = 0  # 余额
# #
# #     if card == card1 and pwd == pwd1:
# #         ban = ban1
# #
# #     elif card == card2 and pwd == pwd2:
# #         ban = ban2
# #     elif card == card3 and pwd == pwd3:
# #         ban = ban3
# #
# #     else:
# #         times = times + 1
# #         if times >= 3:
# #             print("您已经三次输入错误，请联系银行柜台")
# #             break
# #         else:
# #             print("卡号输入错误 请重新输入")
# #             continue
# #
# #     while True:
# #         num = input("请输入要办理的业务:1.存款 2.取款 3.退卡:")
# #         if num == "1":
# #             inn = float(input("请输入存款金额:"))
# #             if inn <= 0:
# #                 print("存款金额请大于0")
# #                 continue
# #             else:
# #                 ban = ban + inn
# #                 print("存款成功！存入:", inn, "余额:", ban)
# #         elif num == "2":
# #             out = float(input("请输入存款金额:"))
# #             if out > ban:
# #                 print("余额不足，请及时充值")
# #                 continue
# #             else:
# #                 ban = ban - out
# #                 print("取款成功！取出:", out, "余额:", ban)
# #         elif num == "3":
# #             print("请收好卡片,欢迎下次再来！")
# #             break
# #         else:
# #             print("输入有误")
# #             continue
# # import time
# #
# # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
#
# # # urlrules
# # website = ''
# # if 'www.' in website:
# #     cutweb = website.split('www.')[1].split('/')[0]
# # elif 'http' in website:
# #     cutweb = website.split('://')[1].split('/')[0]
# # else:
# #     cutweb = website.split('/')[0]
#
# # import requests as r
# # bingurl = ''
# # resp = r.get(url=bingurl)
# # print(resp.text)
# # import time
# # print(time.time())
# # '''https://www.us-proxy.org/'''
# # '''https://www.socks-proxy.net/'''
# # '''https://www.vmall.com/?ANONYMITY_LOGIN_NAME=6021****%40qq.com&ANONYMITY_LOGIN_MOBILE=130****6670'''
# #
# # '''香肠代理账号xc681750'''
# #
#
#
# # 啊
# import requests as r
# import json
#
# # while 1:
# #     resp = r.get('http://121.36.20.177:443/ip_get2?num=10')
# #     result = '{\"https\":\"' + resp.text.replace('\r\n', '\",\n\"http\":\"')[:-10] + '}'
# #     print(result)
# #     proxies = dict(json.loads(result))
# #     print(proxies, type(proxies))
# #     # proxies = {'http': '157.245.57.147:8080'}
# #     # print(proxies, type(proxies))
# #     try:
# #         google = r.get('https://www.google.com/search?q=desk', proxies=proxies, timeout=5).text
# #         with open('ceshi.html', 'w') as f:
# #             f.write(google)
# #             f.close()
# #         print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
# #     except:
# #         print('ip不可用')
# # print(google.text)
#
# # s = '''{"http":"119.131.88.8:9797",
# # "http":"125.78.155.89:9999",
# # "http":"120.83.109.76:9999",
# # "http":"60.12.89.218:33920",
# # "http":"222.124.145.94:8080",
# # "http":"37.187.149.129:1080",
# # "http":"118.172.227.89:33732",
# # "http":"183.166.6.45:9999",
# # "http":"125.123.121.234:9000",
# # "http":"103.78.73.92:3128",
# # "http":"182.34.34.191:9999",
# # "http":"102.176.160.29:44957",
# # "http":"216.198.188.26:51068",
# # "http":"181.126.80.218:3128",
# # "http":"191.240.149.161:8080",
# # "http":"203.142.69.242:47246",
# # "http":"31.163.192.38:43583",
# # "http":"14.98.43.209:80",
# # "http":"183.166.87.31:9999",
# # "http":"103.76.175.85:8080",
# # "http":"101.109.255.243:43426",
# # "http":"58.58.213.55:8888",
# # "http":"117.69.201.19:9999",
# # "http":"49.89.87.31:9999",
# # "http":"178.254.148.231:8090",
# # "http":"222.189.191.241:9999",
# # "http":"1.20.103.135:41594",
# # "http":"120.83.107.137:9999",
# # "http":"124.93.201.59:42672",
# # "http":"191.241.167.251:41288",
# # "http":"103.220.42.165:58456",
# # "http":"125.26.99.241:49650",
# # "http":"185.34.22.225:44050",
# # "http":"109.196.15.142:49133",
# # "http":"77.242.16.26:53281",
# # "http":"123.169.34.152:9999",
# # "http":"182.35.84.3:9999",
# # "http":"120.84.101.5:9999",
# # "http":"222.189.191.137:9999",
# # "http":"171.101.22.238:8118",
# # "http":"36.89.182.3:54295",
# # "http":"1.175.134.251:3128",
# # "http":"114.239.252.161:9999",
# # "http":"92.247.201.112:60419",
# # "http":"1.20.102.102:38816",
# # "http":"101.109.255.48:39560",
# # "http":"182.35.83.185:9999",
# # "http":"46.172.76.114:41562",
# # "http":"94.236.198.183:41258",
# # "http":"182.35.82.44:9999",
# # "http":"190.248.153.162:8080",
# # "http":"179.107.98.18:8080",
# # "http":"95.67.47.94:53281",
# # "http":"185.17.122.185:8080",
# # "http":"89.239.25.218:8080",
# # "http":"117.30.112.213:9999",
# # "http":"103.137.66.17:8080",
# # "http":"27.152.8.112:9999",
# # "http":"5.34.176.14:8080",
# # "http":"182.35.84.193:9999",
# # "http":"190.5.225.178:53570",
# # "http":"59.57.149.218:9999",
# # "http":"105.27.116.46:52075",
# # "http":"202.29.237.213:3128",
# # "http":"31.202.30.118:54547",
# # "http":"176.31.69.182:8080",
# # "http":"176.31.69.183:8080",
# # "http":"118.174.232.181:8080",
# # "http":"5.196.132.122:3128",
# # "http":"176.31.69.177:1080",
# # "http":"183.166.102.27:9999",
# # "http":"120.83.109.134:9999",
# # "http":"113.59.99.138:8910",
# # "http":"49.249.251.86:53281",
# # "http":"117.95.214.236:9999",
# # "http":"1.179.206.201:45294",
# # "http":"173.46.67.172:58517",
# # "http":"196.27.108.175:53281",
# # "http":"188.43.52.166:47362",
# # "http":"59.153.201.66:53281",
# # "http":"200.25.254.193:54240",
# # "http":"117.30.113.168:9999",
# # "http":"47.107.133.109:8000",
# # "http":"60.13.42.68:9999",
# # "http":"109.68.41.78:8080",
# # "http":"103.80.83.161:8080",
# # "http":"168.181.196.71:8080",
# # "http":"159.65.84.239:3128",
# # "http":"1.20.98.66:8080",
# # "http":"45.117.64.3:8080",
# # "http":"112.78.169.98:36963",
# # "http":"84.53.238.49:23500",
# # "http":"188.242.224.144:56391",
# # "http":"154.0.4.180:8080",
# # "http":"103.194.234.129:8080",
# # "http":"182.34.37.32:9999",
# # "http":"58.253.152.167:9999",
# # "http":"212.33.28.51:8080",
# # "http":"50.235.149.74:8080",
# # "http":"84.47.136.146:8080",
# # "http":"186.42.186.202:48281",
# # "http":"60.205.229.126:80",
# # "http":"118.173.233.151:40025",
# # "http":"192.141.12.70:8080",
# # "http":"59.125.31.116:45965",
# # "http":"193.150.117.5:8000",
# # "http":"104.220.227.154:80",
# # "http":"183.164.239.119:9999",
# # "http":"101.132.37.5:8118",
# # "http":"182.35.84.28:9999",
# # "http":"139.194.24.143:8080",
# # "http":"117.57.90.22:9999",
# # "http":"74.15.191.160:41564",
# # "http":"154.7.2.92:3129",
# # "http":"47.106.197.184:8000",
# # "http":"134.35.10.250:8080",
# # "http":"51.79.71.97:80",
# # "http":"201.184.151.58:45718",
# # "http":"103.75.161.38:21776",
# # "http":"118.212.105.0:9999"}'''
# #
# # print(json.loads(s))
#
# # print('If you get error "ImportError: No module named \'six\'" install six:\n' +\ '$ sudo pip install six');
# # print('To enable your free eval account and get CUSTOMER, YOURZONE and ' + \ 'YOURPASS, please contact sales@luminati.io')
# # import sys
# #
# # if sys.version_info[0] == 2: import six
# # # from six.moves.urllib import request
# #
# # # opener = request.build_opener(request.ProxyHandler({'http': 'http://lum-customer-hl_22b1b69a-zone-static:8sd1fto2f79x@zproxy.lum-superproxy.io:22225'}))
# # print(opener.open('http://lumtest.com/myip.json').read())
# #
# # if sys.version_info[0] == 3:
# #     import urllib.request
# #     opener = urllib.request.build_opener(urllib.request.ProxyHandler(
# #     {'http': 'http://lum-customer-hl_22b1b69a-zone-static:8sd1fto2f79x@zproxy.lum-superproxy.io:22225'}))
# # print(opener.open('http://lumtest.com/myip.json').read())
#
#
# # import urllib.request
# #
# # opener = urllib.request.build_opener(
# #     urllib.request.ProxyHandler(
# #         {'http': 'http://lum-customer-hl_22b1b69a-zone-zone1-country-us:ugq8mdlhw7o8@zproxy.lum-superproxy.io:22225'}))
# # print(opener.open('http://lumtest.com/myip.json').read())
# # import urllib.request
#
# # opener = urllib.request.build_opener(
# #     urllib.request.ProxyHandler(
# #         {'http': 'http://lum-customer-hl_0ba1644e-zone-zone1-country-us:3h2xatfe2ks1@zproxy.lum-superproxy.io:22225'}))
# # print(opener.open('http://lumtest.com/myip.json').read())
#
# # res = r.get('http://lumtest.com/myip.json',
# #             proxies={
# #                 'http': 'http://lum-customer-hl_0ba1644e-zone-zone1-country-us:3h2xatfe2ks1@zproxy.lum-superproxy.io:22225'})
# # print(res.text)
#
# # import MySQLdb
# # import requests
# # import json
# # import time
# #
# #
# # def savekw(kw):
# #     conn = MySQLdb.connect(host='47.98.164.255', db='foreign_trade_db', user='root', passwd='Shengshikeji.1',
# #                            charset='utf8')
# #     cursor = conn.cursor()
# #     sql = 'select * from sensitivewords where keyword="{}"'.format(kw)
# #     if '\'' in sql:
# #         sql = sql.replace('\'', '\'\'\'')
# #     if '\"\"' in sql:
# #         sql = sql.replace('\"\"', '\"')
# #     print(sql)
# #     cursor.execute(sql)
# #     result = cursor.fetchall()
# #     if len(result) >= 1:
# #         print('敏感词已存在')
# #         pass
# #     else:
# #         savesql = 'insert into sensitivewords (keyword) values ("{}")'.format(kw)
# #         if '\'' in savesql:
# #             savesql = savesql.replace('\'', '\'\'\'')
# #         if '\"\"' in savesql:
# #             savesql = savesql.replace('\"\"', '\"')
# #         print(savesql)
# #         cursor.execute(savesql)
# #         print('存储成功')
# #         conn.commit()
# #         conn.close()
# #
# #
# # youdaoheaders = {
# #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
# # proxies = {'http': 'http://lum-customer-hl_0ba1644e-zone-zone1-country-us:3h2xatfe2ks1@zproxy.lum-superproxy.io:22225'}
# #
# #
# # def youdaoAPI(kw):
# #     url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
# #
# #     data = {
# #         "i": kw,
# #         "from": "AUTO",
# #         "to": "AUTO",
# #         "smartresult": "dict",
# #         "client": "fanyideskweb",
# #         "salt": "1530598760913",
# #         "sign": "92691936d81b1aaf2316c682773c2012",
# #         "doctype": "json",
# #         "version": "2.1",
# #         "keyfrom": "fanyi.web",
# #         "action": "FY_BY_REALTIME",
# #         "typoResult": "false",
# #     }
# #
# #     response = requests.post(url, data=data, headers=youdaoheaders, proxies=proxies)
# #
# #     # 自带json模块
# #     result = response.json()
# #     result = result['translateResult'][0][0]['tgt']
# #     engresult = result.replace(' ', '')
# #     return engresult
# #
# #
# # def is_Chinese(word):
# #     for ch in word:
# #         if '\u4e00' <= ch <= '\u9fff':
# #             return True
# #     return False
# #
# #
# # # 读文件拿出所有中英文关键字
# # def readfile():
# #     l = ['涉枪涉爆违法信息关键词.txt']  # 文件名
# #     l2 = ['广告.txt', '色情类.txt', '政治类.txt', ]
# #     for fn in l:
# #         print('nnnnnnnn', fn)
# #         with open('{}'.format(fn), 'r') as f:  # 打开一个文件
# #             f.read()
# #             kws = f.read()  # 读取
# #             print(kws)
# #             for kw in kws:  # 一个关键字
# #                 print('判断中英——————————————', kw)
# #             #     if is_Chinese(kw) == True:
# #             #         print('中文，先翻译：', kw)
# #             #         engkw = youdaoAPI(kw)
# #             #         print('翻译之后：', engkw)
# #             #         # 比对数据库
# #             #         if is_Chinese(engkw) == True:
# #             #             engkw = youdaoAPI(engkw)
# #             #             savekw(engkw)
# #             #         savekw(engkw)
# #             #
# #             #     else:
# #             #         print('英文，直接存：', kw)
# #             #         savekw(kw)
# #
# #
# # readfile()
#
# # with open('程序员的一生.png', 'rb') as f:
# #     print(f.read())
#
# import re
# kw = 'mail+@+spppumps.com'
# proxies = {'http': 'http://lum-customer-hl_0ba1644e-zone-zone1-country-us:3h2xatfe2ks1@zproxy.lum-superproxy.io:22225'}
# mailstart = 0
# while mailstart <= 20:
#     try:
#         print(mailstart)
#         searchurl = 'http://www.google.com/search?q={}&start={}'.format(kw, mailstart)
#         resp = r.get(searchurl, proxies=proxies)
#         print(resp)
#         with open('mail.html', 'w') as f:
#             f.write(resp.text)
#             f.close()
#         # if 'did not match any documents' not in resp.text:  # 说明有内容
#         if '找不到和您查询' not in resp.text:  # 说明有内容
#             ts = resp.text
#             rule = re.compile('([a-zA-Z1-9_-]+@\w+\.\w{3,6})')
#             result = rule.findall(ts)
#             mailstart += 10
#             print(result)
#         else:
#             break
#     except:
#         pass

import requests

from lxml import etree

pagenum = 2
url = "https://www.yellow-pages.ph/search/sofa/nationwide/page-{}".format(pagenum)
ret = requests.get(url=url)


e = etree.HTML(ret.content.decode())
# num = e.xpath('/html/body/div[1]/div[1]/div/nav/ol/li[2]/text()')
# print(num)
# num = int(num[0].split("(")[1].split(")")[0]) if num else 0
# print(num)

block_list = e.xpath('//div[@class="search-listing"]')
# print(block_list)
if pagenum > 1:
    block_list = block_list[1:]

li = []
for block in block_list:
    company = block.xpath('.//h2[@class="search-tradename"]/a/text()')[0]
    second_url = "https://www.yellow-pages.ph" + block.xpath('.//h2[@class="search-tradename"]/a/@href')[0]
    print(second_url)
    second_ret = requests.get(second_url)
    # with open('demo2.html', 'wb') as f:
    #     f.write(second_ret.content)
    sec_etree = etree.HTML(second_ret.content.decode())
    main_content = sec_etree.xpath('//div[@class="row"]/div[1]/div[2]/div[3]/div')
    # print(main_content)
    di = {}
    for div in main_content:
        key = div.xpath(".//div[2]/div/text()")[0]
        value = div.xpath(".//div[2]//a//text()")
        val = ""
        for i in value:
            if i.strip():
                val += i + ";"
        val = val[0:-1] if val else val
        di[key] = val
    # print(di)
    address = di.get("Address","")
    landline = di.get("Landline","")
    mobile = di.get("Mobile","")
    phone = landline + ";" + mobile
    phone = phone.strip().strip(";")
    email = di.get("Email","")
    website = di.get("Website","")


    di2 = {}
    di2["company"] = company
    di2["address"] = address
    di2["phone"] = phone
    di2["email"] = email
    di2["website"] = website
    li.append(di2)

print(li)
print(len(li))