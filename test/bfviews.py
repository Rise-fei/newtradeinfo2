from django.http import HttpResponse
from django.shortcuts import render, redirect
import re
import time
import requests as r
from lxml.html import etree
from collections import Counter
from gettrademail.models import KeywordTable, DataTable


def indexp(request):
    return render(request, 'getmail.html')


# Google获取到的信息————————————————————————————————————————————————————————————————————————
def google(kw, start, kwid):
    resp = r.get('https://www.google.com/search?q={}&start={}'.format(kw, start))
    # resp = r.get(ipjiance, proxies=proxies)
    # print(resp.text)
    e = etree.HTML(resp.text)
    titles = e.xpath('//div[@id="main"]/div/div/div/a/div[1]/text()')
    websites = e.xpath('//div[@id="main"]/div/div/div/a/@href')
    descriptions = e.xpath('//div[@id="main"]/div/div/div[3]/div/div/div/div/div/text()')
    objects = zip(titles, websites, descriptions)
    for title, website, description in objects:
        if 'overstock' in website or 'amazon' in website or 'ebay' in website or 'alibaba' in website or 'youtube' in website:
            continue
        elif 'url?q=' in website:
            if 'www.' in website:
                # print(website.split('q=')[1].split('&')[0].split('www.')[1].split('/')[0])
                print(title, website.split('q=')[1].split('&')[0].split('www.')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('q=')[1].split('&')[0].split('www.')[1].split('/')[0])
                if data:
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    infoset.add(website)
            elif 'http' in website:
                # print(website.split('q=')[1].split('&')[0].split('://')[1].split('/')[0])
                print(website)
                print(title, website.split('q=')[1].split('&')[0].split('://')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('q=')[1].split('&')[0].split('://')[1].split('/')[0])
                if data:
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    infoset.add(website)
            else:
                # print(website.split('q=')[1].split('&')[0].split('/')[0])
                print(title, website.split('q=')[1].split('&')[0].split('/')[0], description)
                data = DataTable.objects.filter(website__icontains=website.split('q=')[1].split('&')[0].split('/')[0])
                if data:
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    infoset.add(website)
        else:
            if 'www.' in website:
                # print(website.split('q=')[1].split('&')[0].split('www.')[1].split('/')[0])
                print(title, website.split('www.')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('www.')[1].split('/')[0])
                if data:
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    infoset.add(website)
            elif 'http' in website:
                # print(website.split('q=')[1].split('&')[0].split('://')[1].split('/')[0])
                print(website)
                print(title, website.split('://')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('://')[1].split('/')[0])
                if data:
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    infoset.add(website)
            else:
                # print(website.split('q=')[1].split('&')[0].split('/')[0])
                print(title, website.split('/')[0], description)
                data = DataTable.objects.filter(website__icontains=website.split('q=')[1].split('&')[0].split('/')[0])
                if data:
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    infoset.add(website)


def googleinfo(kw, kwid):
    pagecount = 5  # 从谷歌捕获5页
    print(kw, pagecount)
    if pagecount == 1:
        print('=1')
        googleind = KeywordTable.objects.filter(keyword__iexact=kw)[0].googleind  # 谷歌当前捕获的页数
        print(googleind)
        # pagecount = 0
        google(kw, googleind, kwid)
        KeywordTable.objects.filter(keyword__iexact=kw).googleind = googleind + 1
    else:
        print('>1')
        googleind = KeywordTable.objects.filter(keyword=kw)[0].googleind  # 谷歌当前捕获的页数
        print('当前索引:', googleind)
        for start in range(googleind, pagecount + googleind):
            google(kw, str(start * 10), kwid)
            # print(type(googleind))
            dbkw = KeywordTable.objects.get(keyword__iexact=kw)
            dbkw.googleind = start + 1
            dbkw.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dbkw.save()


# Ask获取到的信息——————————————————————————————————————————————————————————————————————————————————————
def ask(kw, page, kwid):
    # askurl = 'https://www.ask.com/web?q={}&page={}'.format(kw, page)
    askurl = 'https://www.ask.com/web?qo=pagination&q={}&qsrc=998&page={}'.format(kw, page)
    resp = r.get(askurl)
    with open('html.html', 'w') as f:
        f.write(resp.text)
    e = etree.HTML(resp.text)
    titles = e.xpath('//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/text()')
    websites = e.xpath('//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/@href')
    descriptions = e.xpath(
        '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/p[@class="PartialSearchResults-item-abstract"]/text()')
    objects = zip(titles, websites, descriptions)
    for title, website, description in objects:
        print(website)
        if 'overstock' in website or 'amazon' in website or 'ebay' in website or 'alibaba' in website or 'youtube' in website:
            continue
        elif 'www.' in website:
            # print(title, website, description.replace('\n', ' '), '\n', '————————————————————————————————————————————')
            print(website.split('www.')[1].split('/')[0], '\n', '————————————————————————————————————————————')
            DataTable.objects.create(title=title, website=website, description=description,
                                     creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
            infoset.add(website)
        elif 'http' in website:
            print(website.split('://')[1].split('/')[0])
            DataTable.objects.create(title=title, website=website, description=description,
                                     creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
            infoset.add(website)
        else:
            print(website.split('/')[0])
            DataTable.objects.create(title=title, website=website, description=description,
                                     creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
            infoset.add(website)


def askinfo(kw, pagecount, kwid):
    pagecount = 5
    askind = KeywordTable.objects.get(keyword__iexact=kw).askind
    for page in range(askind, askind + pagecount):  # 按页数查询
        ask(kw, str(page), kwid)
        dbkw = KeywordTable.objects.get(keyword__iexact=kw)
        dbkw.askind = page + 1
        dbkw.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        dbkw.save()


# Bing获取到的信息——————————————————————————————————————————————————————————————————————————————————————
class bing():
    def __init__(self, kwlist, count, kwid, start):
        self.url = 'https://cn.bing.com/search?q={}&first={}&ensearch=1'
        self.kwlist = kwlist
        self.count = count
        self.kwid = kwid
        self.start = start
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'accept-encoding': 'utf-8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie': 'DUP=Q=hiH_28VpiCk5fZd2esE9sw2&T=373882886&A=2&IG=E9997C25DD1E4F17A66BFDB8BD6131C8; MUID=3B95B229ACD869DC0076BC2AA8D86A76; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=032EFDA76611481BB2EF2E89FF99762E&dmnchg=1; _EDGE_S=mkt=zh-cn&SID=0103D5820AF563631F48DB8E0BD762A4; ULC=P=1B01B|1:1&H=1B01B|1:1&T=1B01B|1:1; SerpPWA=reg=1; ENSEARCHZOSTATUS=STATUS=0; _FP=hta=on; MUIDB=3B95B229ACD869DC0076BC2AA8D86A76; SNRHOP=I=&TS=; ENSEARCH=BENVER=1; SRCHUSR=DOB=20191106&T=1573028479000; SRCHHPGUSR=CW=1680&CH=868&DPR=2&UTC=480&WTS=63708625279; ipv6=hit=1573032081066&t=6; dsc=order=Maps; _SS=SID=0103D5820AF563631F48DB8E0BD762A4&bIm=60:221&HV=1573028487',
            'referer': 'https://cn.bing.com/search?q=eat+dinner&first=7&FORM=BESBTB',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
        }

    def __gettrueurl(self):
        for kw in self.kwlist:
            self.trueurl = self.url.format(kw.replace(' ', '+'), '{}')
            print(self.trueurl)
            yield self.trueurl

    def getresult(self):
        kwurls = self.__gettrueurl()  # 替换成关键字的URL迭代器
        for kwurl in kwurls:  # 关键字加上页码
            for i in range(self.start, self.start + self.count):
                if i == 1:
                    perpageurl = kwurl.format(str(i))
                    print(perpageurl)
                else:
                    perpageurl = kwurl.format(str((i - 1) * 14))
                    print(perpageurl)
                resp = r.get(perpageurl, headers=self.headers)
                # print(resp.text)
                with open('a.html', 'a+') as f:
                    f.write(resp.text)
                    f.close()
                # print(resp.text)µ
                e = etree.HTML(resp.text)
                elememtscount = len(e.xpath('//ol[@id="b_results"]/li[@class="b_algo"]'))
                for count in range(1, elememtscount + 1):
                    title = e.xpath('string(//ol[@id="b_results"]/li[@class="b_algo"][{}]/h2/a)'.format(str(count)))
                    website = e.xpath(
                        'string(//ol[@id="b_results"]/li[@class="b_algo"][{}]/h2/a/@href)'.format(str(count)))
                    if 'overstock' in website or 'amazon' in website or 'ebay' in website or 'alibaba' in website or 'youtube' in website:
                        continue
                    description = e.xpath(
                        'string(//ol[@id="b_results"]/li[@class="b_algo"][{}]/div/p)'.format(str(count)))
                    if 'www.' in website:
                        # print(title, website.split('www.')[1].split('/')[0], description)
                        print(website.split('www.')[1].split('/')[0])
                        DataTable.objects.create(title=title, website=website, description=description,
                                                 creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 kw_id=self.kwid)
                        infoset.add(website)
                    elif 'http' in website:
                        print(website.split('//')[1].split('/')[0])
                        DataTable.objects.create(title=title, website=website, description=description,
                                                 creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 kw_id=self.kwid)
                        infoset.add(website)
                    else:
                        # print(title, website.split('/')[0], description)
                        print(website.split('/')[0])
                        DataTable.objects.create(title=title, website=website, description=description,
                                                 creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 kw_id=self.kwid)
                        infoset.add(website)
                dbkw = KeywordTable.objects.get(pk=self.kwid)
                dbkw.bingind = i + 1
                dbkw.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                dbkw.save()


def binginfo(kwid, count, *args):
    # bingkws = ['desk', 'dragon', 'qingdao', 'food']
    # pnum = 100  # 消息计数
    # if count < 1:
    #     count = 1
    count = 5
    start = KeywordTable.objects.get(keyword__iexact=args[0]).bingind
    b = bing(args, count, kwid, start)  # bing对象
    b.getresult()


# 获得到的邮箱——————————————————————————————————————————————————
def googlemail(kw):
    mailstart = 0
    while mailstart < 70:
        print(mailstart)
        searchurl = 'http://www.google.com/search?q={}&start={}'.format(kw, mailstart)
        resp = r.get(searchurl)
        with open('test.html', 'w') as f:
            f.write(resp.text)
            f.close()
        # if 'did not match any documents' not in resp.text:  # 说明有内容
        if '找不到和您查询' not in resp.text:  # 说明有内容
            ts = resp.text
            rule = re.compile('([a-zA-Z1-9_-]+@\w+\.\w{3,6})')
            result = rule.findall(ts)
            # print(result)
            mailstart += 10
            yield result
        else:
            start = 0
            break


def gettruest(mails):
    res = [i for item in mails for i in item]
    mdic = Counter(res)
    final = sorted(mdic.items(), key=lambda d: d[1], reverse=True)
    print(len(final))
    print(final)
    if 0 <= len(final) < 3:
        for i in range(len(final)):
            yield final[i][0]
    else:
        for i in range(3):
            yield final[i][0]


def getmail(kwid):  # 拿刚取到的网址来抽取邮箱
    allnone = DataTable.objects.filter(kw_id=kwid, mail=None or '')
    # print(allnone)
    # websites = ['mailto+staples.com']
    for eachnone in allnone:
        website = eachnone.website
        if 'www.' in website:
            newsite = website.split('www.')[1].split('/')[0]
        elif 'http' in website:
            newsite = website.split('://')[1].split('/')[0]
        else:
            newsite = website.split('/')[0]
        newsite = 'mail+@+' + newsite
        print(newsite)
        mails = googlemail(newsite)
        maildata = ';'.join(gettruest(mails))
        # DataTable.objects.get(website=website)
        if len(maildata) > 5:
            eachnone.mail = maildata
            eachnone.creattime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # ###########//
            eachnone.save()
        else:
            continue


def tradeinfo(request):
    # request
    global infoset
    infoset = set()
    # print(request.POST)
    kw = request.POST.get('kw')
    pagecount = 20  # 页数
    dbkw = KeywordTable.objects.filter(keyword__iexact=kw)
    if len(dbkw) == 0:
        print('该关键词不存在')
        KeywordTable.objects.create(keyword=kw, googleind=1, askind=1, bingind=1,
                                    updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        kwid = KeywordTable.objects.get(keyword=kw).id
    else:
        kwid = KeywordTable.objects.get(keyword=kw).id
    # opendb()
    # googleinfo(kw, kwid)
    if len(infoset) < 100:
        print('Google抓完之后集合小于100')
        # askinfo(kw, pagecount, kwid)

    if len(infoset) < 100:
        print('ask抓完之后集合小于100')
        # binginfo(kwid, pagecount, kw)
        pass
    # getmail(kwid)  # 解析网站获得邮箱
    print(infoset, len(infoset))
    results = DataTable.objects.filter(kw_id=kwid, mail__isnull=False).order_by('-creattime')
    return render(request, 'result.html', {'res': results})


defaultnum = 10  # 默认信息条数，当达到阈值则跳出
# tradeinfo()
