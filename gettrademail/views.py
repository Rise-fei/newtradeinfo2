from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.forms.models import model_to_dict
import re
import math
import time
import random
import requests as r
from lxml.html import etree
from collections import Counter
from gettrademail.models import KeywordTable, DataTable
from spiders.ExportIndia import export_india_spider, export_yellowpages_ph,export_europages
from spiders.user_agent_list import user_agent_li
import json
from django.db import connections

def hasCN(string: str):
    """
    判断是否包含汉字(简体中文)
    :param string:
    :return:
    """
    return re.compile(u'[\u4e00-\u9fa5]').search(string)

proxies_data2 =  {'http': 'http://lum-customer-hl_60c2da6c-zone-data_center:fms4eky4mb70@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_60c2da6c-zone-data_center:fms4eky4mb70@zproxy.lum-superproxy.io:22225'}

proxies_data1 = {'http': 'http://lum-customer-hl_60c2da6c-zone-zone1:qx6l05p8ekj5@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_60c2da6c-zone-zone1:qx6l05p8ekj5@zproxy.lum-superproxy.io:22225'}

proxies_data = random.choice([proxies_data1, proxies_data2])
proxies_home = proxies_data

proxies_google_search = {
    'http': 'http://lum-customer-hl_60c2da6c-zone-zone2:tais4r3flqmy@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-hl_60c2da6c-zone-zone2:tais4r3flqmy@zproxy.lum-superproxy.io:22225'
}

proxy_list = [proxies_home, proxies_home, proxies_google_search]
total_headers = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
}
# proxies_data = {}
headers_li = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',

    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',

]


# ***************************************************************
# ***************************************************************
# ***************************************************************
# ***************************************************************

def query_info(website):
    emails = []
    phones = []
    facebooks = []
    twitters = []
    print(111)
    # 得到一个公司官网，查询官网是否有 联系信息！！！
    # resp = r.get(website, headers=headers, proxies=proxies_home)  # 首页的响应信息
    resp = r.get(website, headers=total_headers, proxies=proxies_data)  # 首页的响应信息
    try:
        res = resp.content.decode()
    except:
        res = resp.text

    ret = get_info_from_page(res)

    print('*************************')
    print(ret)
    print('*************************')
    email_list = ret.get('email')
    phone_list = ret.get('phone')
    facebook_list = ret.get('facebook')
    twitter_list = ret.get('twitter')

    emails.extend(email_list)
    phones.extend(phone_list)
    facebooks.extend(facebook_list)
    twitters.extend(twitter_list)

    # 如果没有或者信息不全，爬取官网的 contact us链接 ，继续 寻找内容
    if not emails:
        e = etree.HTML(res)
        contactUs = getContactWeb(website, e)
        print(contactUs)
        if contactUs:
            resp = r.get(contactUs, headers=total_headers, proxies=proxies_data)  # 首页的响应信息
            try:
                res = resp.content.decode()
            except:
                res = resp.text
            ret = get_info_from_page(res)
            print(ret)
            email_list = ret.get('email')
            phone_list = ret.get('phone')
            facebook_list = ret.get('facebook')
            twitter_list = ret.get('twitter')

            emails.extend(email_list)
            phones.extend(phone_list)
            facebooks.extend(facebook_list)
            twitters.extend(twitter_list)

    # 2021.3.19 将getsocial函数和get_email函数结合
    '''
        if not emails:
        if 'www.' in website:
            newsite = website.split('www.')[1].split('/')[0]
        elif 'http' in website:
            newsite = website.split('://')[1].split('/')[0]
        else:
            newsite = website.split('/')[0]
        newsite = 'mail+@+' + newsite
        mails = googlemail2(newsite)
        emails.extend(mails)
    '''


    emails = ";".join(list(set(emails)))
    phones = ";".join(list(set(phones)))
    facebooks = ";".join(list(set(facebooks)))
    twitters = ";".join(list(set(twitters)))
    ret = {
        "email": emails,
        "phone": phones,
        "facebook": facebooks,
        "twitter": twitters,
    }
    print(ret)
    return ret


def get_socials(request):
    '''
    # 对外提供接口，查询某一个网站对应的 邮箱、手机、Facebook、Twitter
    :param request:
    :return: 返回结果字典  { emial:xxxx   phone:xxx   facebook:xxx }
    '''
    print(111)
    website = request.GET.get('website', "")
    print(website)
    if not website:
        return JsonResponse({})
    if 'http' not in website:
        website = 'http://'+ website.strip()

    # 调用爬虫函数进行查询！！！
    try:
        ret = query_info(website)
        print(222)
    except Exception as e:
        print(e)
        ret = {

        }

    return JsonResponse(ret)


def get_page_email(res):
    # 提取邮箱
    email_list = re.findall('([a-zA-Z1-9_-]+@\w+\.\w{3,6})', res)
    # 添加如下
    li = []
    for i in email_list:
        if "xx@xx" not in i:
            li.append(i)
    yield li
    print(email_list)
    return li


def get_page_phone(res):
    # 提取手机号
    s = re.findall(r'>(.*?)<', res)
    s = '#'.join(s)

    ret = re.findall(r'((\+){0,1}( ){0,5}\d{1,4}(( ){0,5}-( ){0,5}\d{1,12})+)', s)
    ret = [i[0] for i in ret if len(i[0]) >= 10]
    if ret:
        pass
    else:
        ret = re.findall(r'((\+){0,1}( {0,5}\d{1,12})+)', s)
        ret = [i[0] for i in ret if len(i[0]) >= 10]
    ret = list(set(ret))
    phone_list = [i.strip() for i in ret]
    print(phone_list)
    return phone_list


def get_page_facebook(res):
    e = etree.HTML(res)
    facebook = e.xpath("//a[contains(@href,'facebook')]/@href")
    facebook_list = list(set(facebook))
    return facebook_list


def get_page_twitter(res):
    e = etree.HTML(res)
    twitter = e.xpath("//a[contains(@href,'twitter')]/@href")
    twitter_list = list(set(twitter))
    return twitter_list


def is_pic(s):
    pic = ['.jpg', '.png', '.bmp', '.tif', '.gif', '.pcx', '.svg', '.psd', '.webp','.txt']
    for p in pic:
        if p in s:
            return True
    return False

def num_counts(s):
    count = 0
    for i in s:
        if i >= '0' and i <= '9':
            count += 1
    return count

def get_info_from_page(res):
    # 获取邮箱
    rule = re.compile('([_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,}))')
    result = rule.findall(res)

    # 添加如下
    email_list = [i[0] for i in result if "xx@xx" not in i[0] and not is_pic(i[0])]
    # 提取手机号

    s = re.findall(r'>(.*?)<', res)
    s = '#'.join(s)
    # regexp = "^(((\\+\\d{2}-)?0\\d{2,3}-\\d{7,8})|((\\+\\d{2}-)?(\\d{2,3}-)?([1][3,4,5,7,8][0-9]\\d{8})))$"
    # rets = re.findall(regexp, s)

    # rets = re.findall(r'((\+){0,1}( ){0,5}\d{1,4}(( ){0,5}-( ){0,5}\d{1,12})+)', s)
    rets = re.findall(r'((\+){0,1}( ){0,5}\d{1,4}(( ){0,5}-{0,1}( ){0,5}\d{1,12})+)', s)


    ret = []
    for i in rets:
        if '+86' not in i[0] and (not i[0].startswith('0086')):
            le = num_counts(i[0])
            if le >= 9 and le <= 18 :
                ret.append(i[0])
    # if ret:
    #     pass
    # else:
    #     ret = re.findall(r'((\+){0,1}( {0,5}\d{1,12})+)', s)
    #     ret = [i[0] for i in ret if len(i[0]) >= 10]
    ret = [i.strip() for i in ret]
    ret = list(set(ret))
    for i in ret:
        if re.match(r'20\d{2}-\d{2}-\d{2}',i):
            ret.remove(i)
    phone_list = ret

    # 获取Facebook
    e = etree.HTML(res)
    facebook = e.xpath("//a[contains(@href,'facebook')]/@href")
    facebook_list = list(set(facebook))

    # 获取Twitter
    e = etree.HTML(res)
    twitter = e.xpath("//a[contains(@href,'twitter')]/@href")
    twitter_list = list(set(twitter))

    ret = {
        'email': email_list,
        'phone': phone_list,
        'facebook': facebook_list,
        'twitter': twitter_list,
    }

    return ret


# ***************************************************************
# ***************************************************************
# ***************************************************************
# ***************************************************************


def yellow_page_nums(request):
    keyword = request.GET.get('keyword')
    cont = request.GET.get('cont', "")


    # 1.印度b2b 搜索  返回结果数量！！
    url = 'https://www.exportersindia.com/search.php?srch_catg_ty=prod&term={}&cont={}'
    url = url.format(keyword, cont)
    headers = {
        "User-Agent": random.choice(user_agent_li),
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }
    ret = r.get(url, headers=total_headers, proxies=proxies_home)
    e = etree.HTML(ret.content.decode('utf-8'))
    num1 = e.xpath('//span[@class="large"]/text()')[0] if e.xpath('//span[@class="large"]/text()') else 0
    num1 = int(num1)
    print("印度的b2b数量：", num1)

    # 2. 菲律宾 黄页搜索   返回结果数量！
    pagenum = 1
    url = "https://www.yellow-pages.ph/search/{}/nationwide/page-{}".format(keyword, pagenum)
    ret = r.get(url=url, headers=total_headers, proxies=proxies_home)

    e = etree.HTML(ret.content.decode())
    num = e.xpath('/html/body/div[1]/div[1]/div/nav/ol/li[2]/text()')
    num2 = int(num[0].split("(")[1].split(")")[0]) if num else 0
    print("菲律宾的黄页数量：", num2)

    # 3.欧洲黄页搜索
    url = "https://www.europages.co.uk/companies/{}.html".format(keyword)
    res = r.get(url=url,headers=total_headers, proxies=proxies_home)
    e = etree.HTML(res.content)
    nums = e.xpath("//div[@class='header-nav']/div/span/h2/span[1]/text()")
    num3 = int(nums[0]) if nums else 0

    ret = {
        'count1': num1,
        'count2': num2,
        'count3':num3,
        'total': num1 + num2 +num3,
    }
    return JsonResponse(ret)


# 查询印度b2b的数量，暂时不用，用上边的那个查
def exportindia_get_total(request):
    keyword = request.GET.get('keyword')
    cont = request.GET.get('cont', "")
    url = 'https://www.exportersindia.com/search.php?srch_catg_ty=prod&term={}&cont={}'
    url = url.format(keyword, cont)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }

    ret = r.get(url, headers=total_headers, proxies=proxies_home)

    e = etree.HTML(ret.content.decode('utf-8'))
    total_count = e.xpath('//span[@class="large"]/text()')[0] if e.xpath('//span[@class="large"]/text()') else 0
    ret = {
        'count': total_count
    }
    return JsonResponse(ret)
    # return HttpResponse(total_count)

def europages(request):
    keyword = request.GET.get('keyword')
    pageno = request.GET.get('pageno', "1")
    print(1111111111)
    print(keyword)
    print(pageno)
    data_list = export_europages(keyword, pageno)
    return JsonResponse({"data": data_list})

def yellowpages_ph(request):
    keyword = request.GET.get('keyword')
    pageno = request.GET.get('pageno', "0")
    print(1111111111)
    print(keyword)
    print(pageno)
    data_list = export_yellowpages_ph(keyword, pageno)
    return JsonResponse({"data": data_list})


def exportindia(request):
    keyword = request.GET.get('keyword')
    pageno = request.GET.get('pageno', "0")
    cont = request.GET.get('cont', "")

    data_list = export_india_spider(keyword, pageno, cont)


    """
   generator = export_india_spider(keyword, pageno, cont, proxies_home)
    
    data_list = []
    for data in generator:
        di = {}
        company, website, addr, phone = data
        if website:
            di["company"] = company
            di["website"] = website
            di["addr"] = addr
            di["phone"] = phone
            # data_list.append(di)


            s = ""
            try:
                s = website + company + addr
            except:
                pass

            if 'china' in s.upper() or 'alibaba' in s.upper():
                continue
            else:
                data_list.append(di)
    """

    return JsonResponse({"data": data_list})


def indexp(request):
    return render(request, 'getmail.html')


def get_mail_from_website(request):
    website = request.GET.get('website')
    print('*********************************')
    print(website)
    if 'www.' in website:
        newsite = website.split('www.')[1].split('/')[0]
    elif 'http' in website:
        newsite = website.split('://')[1].split('/')[0]
    else:
        newsite = website.split('/')[0]
    newsite = 'mail+@+' + newsite
    print('*************')
    print(newsite)
    print('*************')
    mails = googlemail(newsite)

    # print(s)
    # print(list(s))
    maildata = ';'.join(gettruest(mails))
    print('-*-*-**-*-*-*-*-*-*-*-*-*-')
    print(maildata)
    if len(maildata) > 5:
        return HttpResponse(maildata)
    else:
        print('')
        return HttpResponse('no data')


# yahoo 获取到的信息 必要参数关键词和页码
def yahoo(kw, pnum, kwid):
    resp = r.get('https://malaysia.search.yahoo.com/search?p={}&b={}'.format((kw + ' Co.').replace(' ', '+'),
                                                                             (pnum - 1) * 10 + 1), proxies=proxies_data)
    # print(resp.text)
    e = etree.HTML(resp.text)
    datad = []
    sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                 'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook',
                 'twitter', 'dictionary']
    for i in range(len(e.xpath('//div[@id="web"]/ol/li'))):
        title = e.xpath('string(//div[@id="web"]/ol/li[%s]/div/div/h3/a)' % (str(i + 1)))
        website = e.xpath('string(//div[@id="web"]/ol/li[%s]/div/div/h3/a/@href)' % (str(i + 1)))
        description = e.xpath('string(//div[@id="web"]/ol/li[%s]/div/div[2])' % (str(i + 1)))
        print(title, '=======', website, '=======', description)
        if len([i for i in sensitive if i in website]):
            continue
        else:
            if 'www.' in website:
                # print(title, website.split('www.')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website=website, kw_id=kwid)
                if data:
                    datad = datad + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    datad = datad + [{'title': title, 'website': website, 'description': description, 'mail': None}]
            elif 'http' in website:
                # print(title, website.split('://')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('://')[1].split('/')[0], kw_id=kwid)
                if data:
                    datad = datad + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    datad = datad + [{'title': title, 'website': website, 'description': description, 'mail': None}]
            else:
                # print(title, website.split('/')[0], description)
                data = DataTable.objects.filter(website=website, kw_id=kwid)
                if data:
                    datad = datad + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    datad = datad + [{'title': title, 'website': website, 'description': description, 'mail': None}]
        print(datad)
    return datad


# Google获取到的信息————————————————————————————————————————————————————————————————————————
'''

def google(kw, start, kwid):
    headers = {
        'cookie': 'CGIC=Inx0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; ANID=AHWqTUmiVwzKCwVzkajkpZM0NqMGEEZZ20fvp64aF2zCDvs3N7tOdvmtSoEYamQg; OGPC=19016257-10:; OTZ=5372982_24_24__24_; NID=200=K9virnHYIl9GAh5MXnysqfJ3ffAacBYpc9BT7P-zflmkWVWCeP5Awyiwa-AwgkXDxRuVE7ioh0AJnpv3YnbBDgWYacbaj4ovW_QtdW8mnyVGn-8koOO9-d8wvm3JIaTdirfA76kGrf21kfhwZgVnBhfy_wLIA6gEGMQMvL7iU-Q; 1P_JAR=2020-03-20-08',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    resp = r.get('https://www.google.co.in/search?q={}&start={}'.format(kw, start), headers=headers, proxies=proxies)
    print(resp.url)
    # with open('google.html', 'w') as f:
    #     f.write(resp.text)
    #     f.close()
    e = etree.HTML(resp.text)
    titles = e.xpath('//div[@id="rso"]/div/div/div/a/h3/text()')
    websites = e.xpath('//div[@id="rso"]/div/div/div/a/@href')
    descriptions = []
    for i in range(len(titles)):
        description = e.xpath('string(//div[@id="rso"]/div[{}]/div/div[2]/div/span)'.format(str(i + 1)))
        descriptions.append(description)
    objects = zip(titles, websites, descriptions)
    googlel = []
    sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                 'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook', 'twitter',
                 'dictionary']
    for title, website, description in objects:
        print(website)
        if len([i for i in sensitive if i in website]):
            continue
        elif 'url?q=' in website:
            if 'www.' in website:
                # print(title, website.split('q=')[1].split('&')[0].split('www.')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('q=')[1].split('&')[0].split('www.')[1].split('/')[0],
                    kw_id=kwid).order_by('-creattime')
                # 如果数据存在，那么从数据库拿到查询结果返回，否则返回无邮箱电话结果
                if data:
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website.split('url?q=')[1], description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': None}]
            elif 'http' in website:
                # print(title, website.split('q=')[1].split('&')[0].split('://')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('q=')[1].split('&')[0].split('://')[1].split('/')[0],
                    kw_id=kwid).order_by('-creattime')
                if data:
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website.split('url?q=')[1], description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': None}]
            else:
                # print(title, website.split('q=')[1].split('&')[0].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('url?q=')[1].split('&')[0].split('/')[0],
                    kw_id=kwid).order_by('-creattime')
                if data:
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website.split('url?q=')[1], description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': None}]
        else:
            # googlel = googlel + [{'title': title, 'website': website, 'description': description, 'mail': None}]
            if 'www.' in website:
                # print(title, website.split('www.')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('www.')[1].split('/')[0], kw_id=kwid).order_by('-creattime')
                if data:
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': None}]
            elif 'http' in website:
                # print(title, website.split('://')[1].split('/')[0], description)
                data = DataTable.objects.filter(
                    website__icontains=website.split('://')[1].split('/')[0], kw_id=kwid).order_by('-creattime')
                if data:
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': None}]
            else:
                # print(title, website.split('/')[0], description)
                data = DataTable.objects.filter(website__icontains=website.split('q=')[1].split('&')[0].split('/')[0],
                                                kw_id=kwid).order_by('-creattime')
                if data:
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                    continue
                else:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    googlel = googlel + [
                        {'title': title, 'website': website, 'description': description, 'mail': None}]
    return googlel

'''


def google(kw, start, kwid):
    headers = {
        'cookie': 'CGIC=Inx0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; ANID=AHWqTUmiVwzKCwVzkajkpZM0NqMGEEZZ20fvp64aF2zCDvs3N7tOdvmtSoEYamQg; OGPC=19016257-10:; OTZ=5372982_24_24__24_; NID=200=K9virnHYIl9GAh5MXnysqfJ3ffAacBYpc9BT7P-zflmkWVWCeP5Awyiwa-AwgkXDxRuVE7ioh0AJnpv3YnbBDgWYacbaj4ovW_QtdW8mnyVGn-8koOO9-d8wvm3JIaTdirfA76kGrf21kfhwZgVnBhfy_wLIA6gEGMQMvL7iU-Q; 1P_JAR=2020-03-20-08',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    # ************************************************************
    # 2021.2.26谷歌被屏蔽，改用bing看下方
    # resp = r.get('http://www.google.com.hk/search?q={}&start={}'.format(kw, start), headers=headers, proxies=proxies_home)
    # print(resp.url)
    # # with open('demo.html', 'wb') as f:
    # #     f.write(resp.content)
    #
    # e = etree.HTML(resp.text)
    # block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
    # if not block_list:
    #     resp = r.get('http://www.google.com.hk/search?q={}&start={}'.format(kw, start), headers=headers,proxies=proxies_google_search)
    #     e = etree.HTML(resp.text)
    #     block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
    #     if not block_list:
    #         return []

    # print(len(block_list), block_list)
    # print('******************************************')
    # res_list = []
    # for block in block_list:
    #     title = block.xpath('.//h3/span/text()')
    #     print(title)
    #     website = block.xpath('.//div/div/a/@href')
    #     description = block.xpath('string(.//div/div[2]/div/span)')
    #     title = title[0] if title else ""
    #     website = website[0] if website else ""
    #     s = (title, website, description)
    #     res_list.append(s)
    # ************************************************************


    # 2021.2.26
    url = "https://www.bing.com/search?q={}&first={}&count=10".format(kw,start)
    resp = r.get(url, headers={"User-Agent": random.choice(headers_li),},
                 proxies=proxies_data)
    print(resp.url)
    # with open('demo.html', 'wb') as f:
    #     f.write(resp.content)

    e = etree.HTML(resp.text)
    block_list = e.xpath("//li[@class='b_algo']")
    if not block_list:
        print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
        print('精准搜索')
        print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
        url = "https://www.bing.com/search?q={}&first={}&count=10".format(kw, start)
        resp = r.get(url, headers=total_headers,
                     proxies=proxies_home)
        e = etree.HTML(resp.text)
        block_list = e.xpath("//li[@class='b_algo']")
        if not block_list:
            url = "https://www.bing.com/search?q={}&first={}&count=10".format(kw, start)
            resp = r.get(url, headers=total_headers,
                         proxies=proxies_google_search)
            e = etree.HTML(resp.text)
            block_list = e.xpath("//li[@class='b_algo']")
            if not block_list:
                return []
    print('******************************************')
    res_list = []
    for block in block_list:
        title = block.xpath(".//h2/a/text()")
        website = block.xpath(".//h2/a/@href")
        description = block.xpath("string(.//div[@class='b_caption']/p)")
        title = title[0] if title else ""
        website = website[0] if website else ""
        s = (title, website, description)
        res_list.append(s)
    print('******************************************')
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')
    print(res_list)
    print('*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-')

    googlel = []
    sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                 'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook', 'twitter',
                 'dictionary']
    for objects in res_list:
        title, website, description = objects
        print(website)
        if len([i for i in sensitive if i in website]):
            # 如果网址包含 敏感词，直接下一次循环！！！
            print('pass!!!!')
            continue
        # 网址正常，继续判断！
        else:
            # 得到正常网址 website
            if 'url?q=' in website:
                website = website.split('url?q=')[1]
            # 把网址域名拿出来！ rep_icontains
            if 'www.' in website:
                rep_icontains = website.split('www.')[1].split('/')[0]
            elif 'http' in website:
                rep_icontains = website.split('://')[1].split('/')[0]
            else:
                rep_icontains = website.split('/')[0]
            # 将数据库中已经存在的 包含该网址的数据  拿过来！
            data = DataTable.objects.filter(website__icontains=rep_icontains, kw_id=kwid).order_by('-creattime')
            if data:
                googlel = googlel + [
                    {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
            # 如果数据库中不存在该网址，添加进去
            else:
                DataTable.objects.create(title=title, website=website, description=description,
                                         creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                googlel = googlel + [
                    {'title': title, 'website': website, 'description': description, 'mail': None}]
    return googlel


# 首先拿到公司网址的全链接，查看网址中是否有联系我们
def getWebSource(request):
    # u = 'https://www.potterybarn.com/shop/furniture/sofa-sectional-collections/'
    website = request.GET.get('website')
    # 获取到的info仅用于修改

    info = DataTable.objects.filter(website__icontains=website).order_by('-creattime')[0]
    headers = {
        # 'cookie': 'Internationalization=CN|CNY; OriginCountry=CN; tid=UCNzrlOL7mPT3CBNlckDKTVpQcN1zmM8yrb8z05IMWO635u9rhtDANUUinqcZoUZTxRcr8ERmIAJ10Y4_FoLQm-YTii0MyPI-7KBUcRCXHXu0DwQs7_9ZxLt-a_9lQHCbaquQw2; id=kok3zl4qnqaa135r2cmo33cu; Experience=44_A|11_A; zip=60540; zipRemember=60540; uid=6dZ-cylI8UeG46ZkVgqOrw; CBH_CRATEUS=60dvGU2f20GQuIXr5qpzRQ; AKA_A2=A; ak_bmsc=998AC6E50D94755839F099550069462E1720F8C4C40A0000FDEE7A5EC89DF93A~plydCNfTyvdPpkjUtqIh3TpDvqRyKSI1aQjlGNAUQFTtl1mj6DJcTFB815wLlgUI+eWHk3GUdM0e/1uqkCYI1ZRpcs7KFzucO6RuNNve9S9o8NZhwUb1o6JcdakQSQH9YV1LPziYNeBnSKmnNwBdz7d0hiKyQ/wMHPB6UbQv6k8FBYsMWdmgn87HAvI+eP6KC+8xaF4XPWcyYU1TrOrAso+82aNVD8PpxNFZmckoFt5wVHIS6HpTzY839jQi0RVtRG; bm_sz=4778E4CAAB1DD8117B710B5F54DC5895~YAAQxPggF0ZeXMZwAQAAmow1EAfkBSNQDU/6qlNf8QwNKsYX0EyuiD3P4+oAJwJVdp4BaL+FZPjRVDTBGNWiP5wUtbWOpgRjOFi9PR0UlUAtkXgY2TmQZYH6ukrLJW6gIq/cD0PfbARjshT0dCMvuSaofHm1fHw0KpYI+nDOTO9vT/PP7zwvW1JJpbHS80/8WCTSA7MzH10=; optimizelyEndUserId=oeu1585114883721r0.8208182152869226; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22790da0b6-3fd0-4638-87fc-a49626673d1d%22; AMCVS_B9F81C8B5330A6F40A490D4D%40AdobeOrg=1; InternationalWelcome=1; wlcme=true; _ga=GA1.2.1037577580.1585114888; _gid=GA1.2.1407457072.1585114888; _abck=16864C232022F19D2E45962A786D0F10~0~YAAQxPggFwlfXMZwAQAAm7k1EAPIFoA1K5EpXc9izIRhkxxRrUk4yGkHSlY5S1fY9um143yytCh3AlDjArsogNeaLr2RrmZgswxReXZwNIn8oJCPXl6NGYbdtcm7854Cv64uq9Hfr334UpkMH+w7YrdTKrjwwGb3TZswrO3KV7QbQaehOrJ1qoSgnZgSj09rD1mxP/sfNQyUu7dwkVgSKH0zjbgLiw+iguuI4TaIIOpBTmatE3jisj9zx2EGS62Qah7Y1WOahmwbupPH30Bom3iTUI9Ya04lgMc5kdP/rkdaN+o17RFD2hPe53vSs9/MPHEt+sP2YzHUWxWAnveU~-1~-1~-1; basketID=227305865; basketIDRemember=227305865; hasBasket=1; s_ecid=MCMID%7C57774931402568054592901417630552029241; AMCV_B9F81C8B5330A6F40A490D4D%40AdobeOrg=-432600572%7CMCIDTS%7C18347%7CMCMID%7C57774931402568054592901417630552029241%7CMCAAMLH-1585719687%7C11%7CMCAAMB-1585719687%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1585122089s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; BrowseViewTracking=; btpdb.kbMzxFN.dGZjLjQ4OTM1NjQ=REFZUw; D_IID=2C91E143-0507-35B7-B424-2FE71E755AC7; D_UID=2494419D-F06C-3606-AC3D-F1A03213AF80; D_ZID=16717EF8-F8AD-3D61-B141-B51DC34DFB88; D_ZUID=1955B36C-F28A-3617-977C-F7FA3968FF4A; D_HID=444BA707-4174-3C7E-B2D7-74820041F05B; D_SID=119.165.240.85:teyjbEqzEBCauZE2wRqN/DohTbALerwMHMZFwt29DFQ; _gcl_au=1.1.2076564738.1585114890; QuantumMetricUserID=4f553b5e510727227706c977e8c79e20; QuantumMetricSessionID=30423bff1ea53f9c5cfb26afd5c72ff8; cbt-consent-banner=CROSS-BORDER%20Consent%20Banner; _hjid=6cdc3d5c-4850-4ed2-aa4d-e89231ad6327; __RequestVerificationToken=52q5ZZk5CbBrd2M4EFgIqwzWYboR5JtOL-HpIz8GSFN5vouUSE8v3UbHhL5gyti6GTFGKak35Kw43U-kWcPJXqGryBo1; _scid=890b5574-7eab-4f10-81c6-7662a3a3ff8d; s_pers=%20s_ev46%3D%255B%255B%2527Typed%252FBookmarked%2527%252C%25271585114889726%2527%255D%255D%7C1742881289726%3B%20gpv%3Dspill%257Cfurniture%253Aliving%2520room%2520furniture%257Csofas%2520%2526%2520loveseats%7C1585117808092%3B%20s_vs%3D1%7C1585117808108%3B%20s_nr%3D1585116008113-New%7C1616652008113%3B%20s_dl%3D1%7C1585117808116%3B; bm_sv=8DBAC03B0C1677F86F6D74A55609543D~QdU9FCQ4l0xQtkzDLFSGKQnEYWsj21lzYSp4QP4oFW4EpKOLH4RrCVknIQ0YWD7iNNdGUmvx77+SSNXjPtn3Ir4HZ+DjWOeD6bI9IdgarLELEG1h7Kb88ZTkZSANEqjlY8JU2xtZEKoySbYQPfiwl+neO6rAt45kdEnK+NuMt0E=; s_sess=%20cmgvo%3DundefinedTyped%252FBookmarkedTyped%252FBookmarkedundefined%3B%20cpcbrate%3D0%3B%20s_sq%3D%3B%20s_ppvl%3Dspill%25257Cfurniture%25253Aliving%252520room%252520furniture%25257Csofas%252520%252526%252520loveseats%252C72%252C100%252C47608%252C1300%252C875%252C1680%252C1050%252C2%252CL%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dspill%25257Cfurniture%25253Aliving%252520room%252520furniture%25257Csofas%252520%252526%252520loveseats%252C100%252C100%252C47608%252C950%252C875%252C1680%252C1050%252C2%252CL%3B; RT="z=1&dm=crateandbarrel.com&si=5eb7eddb-c45f-4e82-b88f-aee7a311b056&ss=k86wgxi7&sl=3&tt=acuk&bcn=%2F%2F684fc537.akstat.io%2F&ul=1aspo"',
        # 'cookie': 's=30423bff1ea53f9c5cfb26afd5c72ff8; U=4f553b5e510727227706c977e8c79e20',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    # resp = r.get(website, headers=headers, proxies=proxies_home)  # 首页的响应信息
    resp = r.get(website, headers=total_headers, proxies=proxies_data)  # 首页的响应信息
    print('网站获取成功')
    res = resp.text
    e = etree.HTML(res)
    # 捕获是否存在facebook和twitter，如果存在，给下一步一个信号不用捕获了，任何一个不存在则去联系我们找
    # 首页捕获的ft账号信息  {'count': 2, 'result': {'facebook': ['https://www.facebook.com/JohnLewisandPartners'], 'twitter': ['https://twitter.com/JLandPartners']}}
    fat = getFaceAndTwit(e, info)
    print('首次页面抓取结果：', fat)
    pam = getPhoneAndMail(res, info)  # 首页捕获的pm信息,dict, type(value) = 'str'
    print('pam', pam)
    if pam != None:
        if pam['phones']:
            fat['result']['phones'] = pam['phones']
            fat['count'] += 1
        if pam['mails']:
            fat['result']['mails'] = pam['mails']
            fat['count'] += 1
    print(fat)
    if fat['count'] == 4:
        fat = dict(fat)
        return JsonResponse(fat)
    else:
        # 捕获是否有联系我们的链接，返回结果是一个联系我们链接也可能没有
        contactUs = getContactWeb(website, e)
        print('联系我们的链接：', contactUs)
        if contactUs == None:
            fat = dict(fat)
            return JsonResponse(fat)
        else:
            fat['contacturl'] = contactUs
            # 存在联系我们的链接，且数据不够完全访问此链接并进行数据补充
            fat = getContactUs(contactUs, fat, info)
    print('fat:', type(fat), fat)
    fat = dict(fat)
    return JsonResponse(fat)


def getFaceAndTwit(e, info):
    facebook = e.xpath("//a[contains(@href,'facebook')]/@href")
    twitter = e.xpath("//a[contains(@href,'twitter')]/@href")
    if facebook and twitter:
        info.remark2 = facebook[0]
        info.remark3 = twitter[0]
        info.save()
        return {'count': 2, 'result': {'facebook': facebook[0], 'twitter': twitter[0]}}
    elif facebook:
        info.remark2 = facebook[0]
        info.save()
        return {'count': 1, 'result': {'facebook': facebook[0], 'twitter': ''}}
    elif twitter:
        info.remark3 = twitter[0]
        info.save()
        return {'count': 1, 'result': {'facebook': '', 'twitter': twitter[0]}}
    else:
        return {'count': 0, 'result': {'facebook': '', 'twitter': ''}}


def getPhoneAndMail(res, info):
    pat = re.compile('>(.*?)<')
    s = ' '.join(pat.findall(res))
    ap = []
    phone1 = re.findall(r'\(\d{3}\) ?\d{6}', s)
    phone2 = re.findall(r'\d{5} {1}\d{6}|\d{6} {1}\d{5}', s)
    phone3 = re.findall(r'\d{3}-\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4}', s)
    phone4 = re.findall(r'\d{5} \d{3} \d{3}', s)
    phone5 = re.findall(r'\(\d{3}\) ?\d{3}-\d{4}', s)
    phone6 = re.findall(r'\+[0-9 \(\)-.]{6,}', s)
    phone7 = re.findall(r'(\(\d{2}\) \d{4} \d{4})', s)
    phone8 = re.findall(r'(\d{4} \d{4} \d{3})', s)
    # phone8 = re.findall(r'(\d{2} \d{2} \d{4}) \d{4}', s)
    ap.extend(phone1)
    ap.extend(phone2)
    ap.extend(phone3)
    ap.extend(phone4)
    ap.extend(phone5)
    ap.extend(phone6)
    ap.extend(phone7)
    ap.extend(phone8)
    # print('phoneType1:', phone1)
    # print('phoneType2:', phone2)
    # print('phoneType3:', phone3)
    # print('phoneType4:', phone4)
    # print('phoneType5:', phone5)
    print('phoneType6:', phone6)
    mails = re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+)', s)
    hps = Counter(ap)
    mls = Counter(mails)
    # print('phoneAll:', [pk for pk, pv in hps.items() if len(hps.items()) > 5 and pv > 2 or pv])
    # # 判断如果总数大于5并且存在数量大于2则保存并且字符串不在key中
    # print('mailAll:', [mk for mk, mv in mls.items() if len(
    #     mls.items()) > 5 and mv > 2 and '.jpg' not in mk and '.io' not in mk and '.jpeg' not in mk and mv and '.jpg' not in mk and '.io' not in mk])
    phoneAll = ';'.join([pk for pk, pv in hps.items() if len(hps.items()) > 5 and pv > 2 or pv])
    # mailAll = ';'.join([mk for mk, mv in mls.items() if len(
    #     mls.items()) > 5 and mv > 2 and '.jpg' not in mk and '.io' not in mk and '.jpeg' not in mk and mv and '.jpg' not in mk and '.io' not in mk])
    mailAll = ';'.join([mk for mk, mv in mls.items() if len(
        mls.items()) > 5 and mv > 2 and '.jpg' not in mk and '.io' not in mk and '.jpeg' not in mk or mv and '.jpg' not in mk and '.io' not in mk and '.jpeg' not in mk])
    if len(phoneAll) != 0 and len(mailAll) != 0:
        if len(mailAll) != 0:
            info.mail = mailAll
        if len(phoneAll) != 0:
            info.remark1 = phoneAll
        info.save()
        return {'phones': phoneAll, 'mails': mailAll}
    else:
        return None


# 如果有拿到联系我们的链接
def getContactWeb(u, e):
    contact1 = e.xpath("//a[contains(text(),'contact')]/@href")
    contact2 = e.xpath("//a[contains(text(),'Contact')]/@href")
    contact3 = e.xpath("//a[contains(text(),'CONTACT')]/@href")
    contact = contact2 + contact1 + contact3
    fres = Counter(contact).keys()
    print(fres)
    if len(fres) == 0:
        return None
    else:
        u = u.split('/')[0] + '//' + [eve for eve in u.split('/')][2]
        for fr in fres:
            if fr.startswith('/'):
                if u.endswith('/'):
                    fr = u + fr[1:]
                else:
                    fr = u + fr
            return fr


def getContactUs(contactwebsite, fat, info):
    print('从联系我们抓取数据···')
    headers = {
        'cookie': 'Internationalization=CN|CNY; OriginCountry=CN; tid=UCNzrlOL7mPT3CBNlckDKTVpQcN1zmM8yrb8z05IMWO635u9rhtDANUUinqcZoUZTxRcr8ERmIAJ10Y4_FoLQm-YTii0MyPI-7KBUcRCXHXu0DwQs7_9ZxLt-a_9lQHCbaquQw2; id=kok3zl4qnqaa135r2cmo33cu; Experience=44_A|11_A; zip=60540; zipRemember=60540; uid=6dZ-cylI8UeG46ZkVgqOrw; CBH_CRATEUS=60dvGU2f20GQuIXr5qpzRQ; AKA_A2=A; ak_bmsc=998AC6E50D94755839F099550069462E1720F8C4C40A0000FDEE7A5EC89DF93A~plydCNfTyvdPpkjUtqIh3TpDvqRyKSI1aQjlGNAUQFTtl1mj6DJcTFB815wLlgUI+eWHk3GUdM0e/1uqkCYI1ZRpcs7KFzucO6RuNNve9S9o8NZhwUb1o6JcdakQSQH9YV1LPziYNeBnSKmnNwBdz7d0hiKyQ/wMHPB6UbQv6k8FBYsMWdmgn87HAvI+eP6KC+8xaF4XPWcyYU1TrOrAso+82aNVD8PpxNFZmckoFt5wVHIS6HpTzY839jQi0RVtRG; bm_sz=4778E4CAAB1DD8117B710B5F54DC5895~YAAQxPggF0ZeXMZwAQAAmow1EAfkBSNQDU/6qlNf8QwNKsYX0EyuiD3P4+oAJwJVdp4BaL+FZPjRVDTBGNWiP5wUtbWOpgRjOFi9PR0UlUAtkXgY2TmQZYH6ukrLJW6gIq/cD0PfbARjshT0dCMvuSaofHm1fHw0KpYI+nDOTO9vT/PP7zwvW1JJpbHS80/8WCTSA7MzH10=; optimizelyEndUserId=oeu1585114883721r0.8208182152869226; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22790da0b6-3fd0-4638-87fc-a49626673d1d%22; AMCVS_B9F81C8B5330A6F40A490D4D%40AdobeOrg=1; InternationalWelcome=1; wlcme=true; _ga=GA1.2.1037577580.1585114888; _gid=GA1.2.1407457072.1585114888; _abck=16864C232022F19D2E45962A786D0F10~0~YAAQxPggFwlfXMZwAQAAm7k1EAPIFoA1K5EpXc9izIRhkxxRrUk4yGkHSlY5S1fY9um143yytCh3AlDjArsogNeaLr2RrmZgswxReXZwNIn8oJCPXl6NGYbdtcm7854Cv64uq9Hfr334UpkMH+w7YrdTKrjwwGb3TZswrO3KV7QbQaehOrJ1qoSgnZgSj09rD1mxP/sfNQyUu7dwkVgSKH0zjbgLiw+iguuI4TaIIOpBTmatE3jisj9zx2EGS62Qah7Y1WOahmwbupPH30Bom3iTUI9Ya04lgMc5kdP/rkdaN+o17RFD2hPe53vSs9/MPHEt+sP2YzHUWxWAnveU~-1~-1~-1; basketID=227305865; basketIDRemember=227305865; hasBasket=1; s_ecid=MCMID%7C57774931402568054592901417630552029241; AMCV_B9F81C8B5330A6F40A490D4D%40AdobeOrg=-432600572%7CMCIDTS%7C18347%7CMCMID%7C57774931402568054592901417630552029241%7CMCAAMLH-1585719687%7C11%7CMCAAMB-1585719687%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1585122089s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; BrowseViewTracking=; btpdb.kbMzxFN.dGZjLjQ4OTM1NjQ=REFZUw; D_IID=2C91E143-0507-35B7-B424-2FE71E755AC7; D_UID=2494419D-F06C-3606-AC3D-F1A03213AF80; D_ZID=16717EF8-F8AD-3D61-B141-B51DC34DFB88; D_ZUID=1955B36C-F28A-3617-977C-F7FA3968FF4A; D_HID=444BA707-4174-3C7E-B2D7-74820041F05B; D_SID=119.165.240.85:teyjbEqzEBCauZE2wRqN/DohTbALerwMHMZFwt29DFQ; _gcl_au=1.1.2076564738.1585114890; QuantumMetricUserID=4f553b5e510727227706c977e8c79e20; QuantumMetricSessionID=30423bff1ea53f9c5cfb26afd5c72ff8; cbt-consent-banner=CROSS-BORDER%20Consent%20Banner; _hjid=6cdc3d5c-4850-4ed2-aa4d-e89231ad6327; __RequestVerificationToken=52q5ZZk5CbBrd2M4EFgIqwzWYboR5JtOL-HpIz8GSFN5vouUSE8v3UbHhL5gyti6GTFGKak35Kw43U-kWcPJXqGryBo1; _scid=890b5574-7eab-4f10-81c6-7662a3a3ff8d; s_pers=%20s_ev46%3D%255B%255B%2527Typed%252FBookmarked%2527%252C%25271585114889726%2527%255D%255D%7C1742881289726%3B%20gpv%3Dspill%257Cfurniture%253Aliving%2520room%2520furniture%257Csofas%2520%2526%2520loveseats%7C1585117808092%3B%20s_vs%3D1%7C1585117808108%3B%20s_nr%3D1585116008113-New%7C1616652008113%3B%20s_dl%3D1%7C1585117808116%3B; bm_sv=8DBAC03B0C1677F86F6D74A55609543D~QdU9FCQ4l0xQtkzDLFSGKQnEYWsj21lzYSp4QP4oFW4EpKOLH4RrCVknIQ0YWD7iNNdGUmvx77+SSNXjPtn3Ir4HZ+DjWOeD6bI9IdgarLELEG1h7Kb88ZTkZSANEqjlY8JU2xtZEKoySbYQPfiwl+neO6rAt45kdEnK+NuMt0E=; s_sess=%20cmgvo%3DundefinedTyped%252FBookmarkedTyped%252FBookmarkedundefined%3B%20cpcbrate%3D0%3B%20s_sq%3D%3B%20s_ppvl%3Dspill%25257Cfurniture%25253Aliving%252520room%252520furniture%25257Csofas%252520%252526%252520loveseats%252C72%252C100%252C47608%252C1300%252C875%252C1680%252C1050%252C2%252CL%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dspill%25257Cfurniture%25253Aliving%252520room%252520furniture%25257Csofas%252520%252526%252520loveseats%252C100%252C100%252C47608%252C950%252C875%252C1680%252C1050%252C2%252CL%3B; RT="z=1&dm=crateandbarrel.com&si=5eb7eddb-c45f-4e82-b88f-aee7a311b056&ss=k86wgxi7&sl=3&tt=acuk&bcn=%2F%2F684fc537.akstat.io%2F&ul=1aspo"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    contactResp = r.get(contactwebsite, headers=total_headers, proxies=proxies_data).text
    contacte = etree.HTML(contactResp)
    # fat = 1说明Facebook和Twitter信息没采集完全
    print(fat['result'].keys(), '=========================')
    noget = [i for i in ['facebook', 'twitter', 'phones', 'mails'] if i not in fat['result'].keys()]
    if 'facebook' in noget or 'twitter' in noget:
        contactFAT = getFaceAndTwit(contacte, info)
        contactface = contactFAT['result']['facebook']
        contacttwit = contactFAT['result']['twitter']
        fat['result']['facebook'] = contactface
        fat['result']['twitter'] = contacttwit
        print(fat['result'])
    elif 'phones' in noget or 'mails' in noget:
        contactPAM = getPhoneAndMail(contactResp, info)
        if contactPAM == None:
            fat['result']['phones'] = ''
            fat['result']['mail'] = ''
        else:
            fat['result']['phones'] = contactPAM['phones']
            fat['result']['mails'] = contactPAM['mails']
    return fat


# 当调用这个的时候从网站源码中获取邮箱和电话（website必须是完整链接）
def getPaM(request):
    website = request.GET.get('website')
    info = DataTable.objects.filter(website__icontains=website).order_by('-creattime')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
    }
    try:
        resp = r.get(website, headers=total_headers, proxies=proxies_data)
        # print(resp.text)
        resp = resp.content.decode(resp.encoding)
        pat = re.compile('>(.*?)<')
        s = ' '.join(pat.findall(resp))
        ap = []
        phone1 = re.findall(r'\(\d{3}\) ?\d{6}', s)
        phone2 = re.findall(r'\d{5} {1}\d{6}|\d{6} {1}\d{5}', s)
        phone3 = re.findall(r'\d{3}-\d{3}-\d{4}|\d{3}\.\d{3}\.\d{4}', s)
        phone4 = re.findall(r'\d{5} \d{3} \d{3}', s)
        phone5 = re.findall(r'\(\d{3}\) ?\d{3}-\d{4}', s)
        phone6 = re.findall(r'\+[0-9 \(\)-.]{6,}', s)
        ap.extend(phone1)
        ap.extend(phone2)
        ap.extend(phone3)
        ap.extend(phone4)
        ap.extend(phone5)
        ap.extend(phone6)
        # print('phoneType1:', phone1)
        # print('phoneType2:', phone2)
        # print('phoneType3:', phone3)
        # print('phoneType4:', phone4)
        # print('phoneType5:', phone5)
        # print('phoneType6:', phone6)
        mails = re.findall(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+)', s)
        hps = Counter(ap)
        mls = Counter(mails)
        print('phoneAll:', [pk for pk, pv in hps.items() if len(hps.items()) > 5 and pv > 2 or pv])
        print('mailAll:', [mk for mk, mv in mls.items() if len(
            mls.items()) > 5 and mv > 2 and '.jpg' not in mk and '.io' not in mk or mv and '.jpg' not in mk and '.io' not in mk])
        phoneAll = ';'.join([pk for pk, pv in hps.items() if len(hps.items()) > 5 and pv > 2 or pv])
        mailAll = ';'.join([mk for mk, mv in mls.items() if len(
            mls.items()) > 5 and mv > 2 and '.jpg' not in mk and '.io' not in mk or mv and '.jpg' not in mk and '.io' not in mk])
        info[0].mail = mailAll
        info[0].remark1 = phoneAll
        info[0].save()
        if len(phoneAll) != 0 or len(mailAll) != 0:
            return JsonResponse({'phones': phoneAll, 'mails': mailAll})
        else:
            return HttpResponse(None)
    except:
        print('Error')
        return HttpResponse(None)


def googleinfo(kw, kwid, pagenum):
    googleresult = google(kw, str(pagenum * 10), kwid)
    # [{}{}{}{}]
    print('********************************')
    print(googleresult)
    print('********************************')
    dbkw = KeywordTable.objects.get(keyword__iexact=kw)
    dbkw.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dbkw.save()
    return googleresult


def google_spider(url):
    pro_list = [(proxies_data1, '数据中心1'), (proxies_data2, '数据中心2')]
    proo_list = random.choices(pro_list, k=2)
    proxy_list = proo_list + [
        (proxies_home, "动态住宅"), (proxies_google_search, "搜索引擎"), ({}, '无')]
    # print(proxy_list)
    block_list = []
    for proxies in proxy_list:
        resp = r.get(url, proxies=proxies[0], headers={"User-Agent": random.choice(headers_li), })
        # resp = r.get(url, proxies={}, headers={"User-Agent": random.choice(headers_li), })
        # with open("a.html", 'wb') as f:
        #     f.write(resp.content)
        e = etree.HTML(resp.text)
        block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        # block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        if block_list:
            # with open('111.html','wb') as f:
            #     f.write(resp.content)
            print('爬虫获得结果，用到代理为：%s' % proxies[1])
            return block_list
    return block_list


def new_googleinfo(kw, num):
    # num = 1 2 3 4 5 6 7 8 ... 100
    headers = {
        'cookie': 'CGIC=Inx0ZXh0L2h0bWwsYXBwbGljYXRpb24veGh0bWwreG1sLGFwcGxpY2F0aW9uL3htbDtxPTAuOSxpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; ANID=AHWqTUmiVwzKCwVzkajkpZM0NqMGEEZZ20fvp64aF2zCDvs3N7tOdvmtSoEYamQg; OGPC=19016257-10:; OTZ=5372982_24_24__24_; NID=200=K9virnHYIl9GAh5MXnysqfJ3ffAacBYpc9BT7P-zflmkWVWCeP5Awyiwa-AwgkXDxRuVE7ioh0AJnpv3YnbBDgWYacbaj4ovW_QtdW8mnyVGn-8koOO9-d8wvm3JIaTdirfA76kGrf21kfhwZgVnBhfy_wLIA6gEGMQMvL7iU-Q; 1P_JAR=2020-03-20-08',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    # proxies = random.choice(proxy_list)
    proxies = proxies_google_search

    # 本地测试！！
    # proxies={}
    country_code = ['UA', 'JP', 'KR', 'IN', 'DE', 'NL', 'GB', 'SG', 'CA', 'RU', 'MY',
                    'VN', 'LA', 'BR', 'RU','AF', 'AR', 'AE','SR', 'AZ', 'SN', 'SE', 'IR','MT', 'TT', 'PT', 'NG',
                    'DZ', 'AG', 'KP', 'GA', 'GI',
                    'VE', 'MU', 'ML', 'MO', 'ID',
                    'VN', 'TO', 'TM', 'EC', 'NR',
                    'PY', 'BW', 'SO', 'SY', 'CL',
                    'SM', 'MC', 'IT', 'BR',
                    'BI', 'PE', 'SD', 'YU',
                    'FR', 'KW', 'UZ',
                    'FI', 'GU', 'MM', 'DJ',
                    'AU', 'BM', 'KH', 'CK', 'BO',
                    'BZ', 'TG', 'HT', 'UY', 'SV',
                    'BB', 'ST', 'NP', 'TN', 'ZW',
                    'PR', 'IL', 'KG', 'CH',
                    'HK', 'YE', 'LV', 'MN', 'CY',
                    'ZA', 'LY', 'CU', 'DK', 'MD',
                    'BH', 'BF', 'LB', 'ZR', 'RO',
                    'IQ', 'DO', 'ES', 'CF',
                    'LK', 'SA', 'BE', 'ZM', 'AO',
                    'MV', 'MS', 'NO', 'PL',
                    'SK', 'AD', 'TW', 'AM', 'TJ',
                    'MG', 'GN', 'FJ', 'LU', 'NZ',
                    'GH', 'MZ', 'PA', 'GM', 'LC',
                    'GT', 'BD', 'BS', 'EG', 'TR',
                    'UG', 'AI', 'NA', 'TH', 'IE',
                    'SZ', 'BJ', 'CG', 'LA',
                    'QA', 'SB', 'SI',
                    'AT', 'JO', 'CN', 'BN', 'GY',
                    'PK', 'VC', 'CR', 'US', 'GF',
                    'LR', 'BG', 'TZ', 'CO',
                    'LI', 'IS', 'GR', 'OM',
                    'GE', 'KE', 'PF', 'HU', 'ET',
                    'GD', 'MA', 'LS', 'BY', 'AL',
                    'CM', 'SL', 'MX', 'JM', 'EE',
                    'PH', 'PG', 'CZ', 'HN', 'MW',
                    'SC', 'KZ', 'LT', 'NI', 'TD']
    # country_code = random.shuffle(country_code)


    country_engine1 = ['www.google.nl', 'www.google.com', 'www.google.com.mx', 'www.google.no',
                      'www.google.de', 'www.google.ru', 'www.google.fi', 'www.google.pl', 'www.google.it',
                      'www.google.pt', 'www.google.es', 'www.google.la', 'www.google.se', 'www.google.dk',
                      'www.google.fr', 'www.google.com.kh', 'www.google.co.uk', 'www.google.com.vn', 'www.google.co.jp',
                      'www.google.co.th', 'www.google.com.my', 'www.google.com.sg', 'www.google.com.bn',
                      'www.google.com.ph', 'www.google.co.id', 'www.google.co.in', 'www.google.com.pk',
                      'www.google.co.ke', 'www.google.com.na', 'www.google.im', 'www.google.co.kr', 'www.google.sc',
                      'www.google.md', 'www.google.st', 'www.google.com.au', 'www.google.com.bd', 'www.google.com.tw',
                      'www.google.is', 'www.google.com.uy', 'www.google.com.ai', 'www.google.com.et',
                      'www.google.com.ar', 'www.google.ms', 'www.google.gy', 'www.google.gg', 'www.google.bg',
                      'www.google.co.zm', 'www.google.be', 'www.google.com.tj', 'www.google.li', 'www.google.com.gt',
                      'www.google.hu', 'www.google.com.bh', 'www.google.mw', 'www.google.si', 'www.google.com.bo',
                      'www.google.to', 'www.google.com.co', 'www.google.ci', 'www.google.mv', 'www.google.ht',
                      'www.google.bs', 'www.google.co.ma', 'www.google.mn', 'www.google.com.br', 'www.google.ws',
                      'www.google.nr', 'www.google.com.gi', 'www.google.com.nf', 'www.google.com.sa',
                      'www.google.co.ve', 'www.google.com.sv', 'www.google.co.ls', 'www.google.co.za',
                    ]

    country_engine2 = [  'www.google.co.cr', 'www.google.com.sb', 'www.google.co.vi', 'www.google.lv', 'www.google.lu',
                      'www.google.gr', 'www.google.com.pe', 'www.google.ie', 'www.google.dm', 'www.google.tp',
                      'www.google.gm', 'www.google.com.mt', 'www.google.co.yu', 'www.google.cz', 'www.google.com.np',
                      'www.google.com.ni', 'www.google.com.tr', 'www.google.ch', 'www.google.co.il', 'www.google.tm',
                      'www.google.tt', 'www.google.je', 'www.google.sk', 'www.google.com.ec', 'www.google.com.pa',
                      'www.google.bi', 'www.google.tk', 'www.google.gp', 'www.google.as', 'www.google.nu',
                      'www.google.com.vc', 'www.google.hr', 'www.google.ki', 'www.google.am', 'www.google.com.eg',
                      'www.google.com.af', 'www.google.fm', 'www.google.com.fj', 'www.google.com.pr',
                      'www.google.co.ug', 'www.google.com.ly', 'www.google.com.jm', 'www.google.ee', 'www.google.cd',
                      'www.google.sm', 'www.google.co.bw', 'www.google.co.nz', 'www.google.pn', 'www.google.ge',
                      'www.google.lt', 'www.google.com.ag', 'www.google.com.by', 'www.google.lk', 'www.google.co.uz',
                      'www.google.cg', 'www.google.com.ua', 'www.google.ro', 'www.google.com.ng', 'www.google.com.do',
                      'www.google.ae', 'www.google.com.bz', 'www.google.com.cu', 'www.google.dj', 'www.google.kg',
                      'www.google.vg', 'www.google.gl', 'www.google.com.py', 'www.google.az', 'www.google.vu',
                      'www.google.rw', 'www.google.sh', 'www.google.at', 'www.google.mu', 'www.google.ca',
                      'www.google.co.ck', 'www.google.com.qa', 'www.google.jo', 'www.google.co.zw', 'www.google.com.om',
                      'www.google.kz', 'www.google.cl', 'www.google.ba', 'www.google.sn','www.google.com.hk']

    # country_engine = random.choice([country_engine1,country_engine2])
    country_engine = country_engine1
    length = len(country_engine)
    # 第 n 个 ， 用第n个 搜索引擎
    engine_index = num % length
    engine = country_engine[engine_index]

    round = math.ceil(num / length)
    googlel = []
    # 1 2 3     1      4 5 6     2       7 8 9    3
    # num = 1    1  [1]        0-100
    #  2         1  [1]        100-200
    #  3         2  [1.5]         0-100
    #  4         2  [2]         100-200
    #  5         3  [2.5]          0-100
    #  6         3  [3]         100-200
    c_engine = random.choice(country_engine1)
    index = math.ceil(num / 3)
    c_code = country_code[index-1]
    if num % 3 == 2:
        url = 'http://{}/search?q={}&start=0&num=100&cr=country{}'.format(c_engine,kw,c_code)
    elif num % 3 == 1:
        url = 'http://{}/search?q={}&start=0&num=100&cr=country{}'.format(c_engine, kw, c_code)
    else:
        url = 'http://{}/search?q={}&start=0&num=100&cr=country{}'.format(c_engine,kw,c_code)
    try:
        # url = 'http://{}/search?q={}&start=0&num=100&cr=country{}'.format(c_engine,kw,c_code)
        # -----------------------------------------------
        # url = 'http://{}/search?q={}&start={}&num=100'.format(engine, kw, (round - 1) * 100)
        # url = 'http://{}/search?q="{}"&start={}&num=100'.format(engine, kw, (round - 1) * 100)
        print(url)

        block_list = google_spider(url)
        # ra = random.randint(1,4)
        # if ra < 4:
        #     resp = r.get(url, headers={"User-Agent": random.choice(headers_li),}, proxies=proxies_home)
        #     print('***************home proxy*******************')
        #     # resp = r.get('http://www.google.com.hk/search?q="{}"&start={}'.format(kw, str(pagenum * 10)), headers=headers, proxies=proxies)
        #     # resp = r.get('http://www.google.com.hk/search?q="{}"&start={}'.format(kw, str(pagenum * 10)), headers=headers, proxies={})
        #
        #     print(resp.url)
        #     # with open('demo.html', 'wb') as f:
        #     #     f.write(resp.content)
        #     e = etree.HTML(resp.text)
        #     block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        #     print(len(block_list))
        #     print('******************************************')
        # else:
        #     block_list = None
        # if not block_list:
        #     print('***************google search proxy*******************')
        #     resp = r.get(url, headers={"User-Agent": random.choice(headers_li), }, proxies=proxies_google_search)
        #     e = etree.HTML(resp.text)
        #     block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        #     print(len(block_list))
        #     print('******************************************')
        res_list = []
        for block in block_list:
            title = block.xpath('.//h3/text()')
            # print(title)
            website = block.xpath('./div/div[1]/div[1]/a/@href')
            description = block.xpath('string(./div/div[2]//span)')
            # description = " ".join(description)
            title = title[0] if title else ""
            website = website[0] if website else ""
            s = (title, website, description)
            # print(s)

            if not title:
                continue
            if not website:
                continue

            if not hasCN(title+website+description):
                print("没有中文 添加！！")
                res_list.append(s)
            else:
                print("有中文，不加！")

        print('******************************************')

        sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                     'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook', 'twitter',
                     'dictionary','china','taobao','edu','gov','china','GOV','EDU','CHINA']
        for objects in res_list:
            title, website, description = objects
            # print(website)
            if len([i for i in sensitive if i in website]):
                # 如果网址包含 敏感词，直接下一次循环！！！
                print('pass!!!!')
                continue
            # 网址正常，继续判断！
            else:
                # 得到正常网址 website
                if 'url?q=' in website:
                    website = website.split('url?q=')[1]
                googlel.append({'title': title, 'website': website, 'description': description, 'mail': None})
    except Exception as e:
        print(e)

    if not googlel:
        with open('error_engine.txt','a') as f:
            f.write(str(engine))
            f.write(',')
    if not googlel:
        with open('error_engine2.txt','a') as f:
            f.write(str(engine)+"---"+str(proxies))
            f.write('\n')
    return googlel


# Ask获取到的信息——————————————————————————————————————————————————————————————————————————————————————
def ask(kw, page, kwid):
    kw = kw.replace(' ', '%20')
    askurl = 'https://www.ask.com/web?qo=pagination&q={}&qsrc=998&page={}'.format(kw, page)
    resp = r.get(askurl, proxies=proxies_data)
    # with open('ask.html', 'w') as f:
    #     f.write(resp.text)
    e = etree.HTML(resp.text)
    titles = e.xpath('//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/text()')
    websites = e.xpath('//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/@href')
    descriptions = e.xpath(
        '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/p[@class="PartialSearchResults-item-abstract"]/text()')
    objects = zip(titles, websites, descriptions)
    if not titles:
        resp = r.get(askurl, proxies=proxies_home)
        # with open('ask.html', 'w') as f:
        #     f.write(resp.text)
        e = etree.HTML(resp.text)
        titles = e.xpath(
            '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/text()')
        websites = e.xpath(
            '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/@href')
        descriptions = e.xpath(
            '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/p[@class="PartialSearchResults-item-abstract"]/text()')
        objects = zip(titles, websites, descriptions)
        if not titles:
            resp = r.get(askurl, proxies=proxies_google_search)
            # with open('ask.html', 'w') as f:
            #     f.write(resp.text)
            e = etree.HTML(resp.text)
            titles = e.xpath(
                '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/text()')
            websites = e.xpath(
                '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/div/a/@href')
            descriptions = e.xpath(
                '//div[@class="PartialSearchResults-body"]/div[@class="PartialSearchResults-item"]/p[@class="PartialSearchResults-item-abstract"]/text()')
            objects = zip(titles, websites, descriptions)

    datad = []
    sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                 'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook',
                 'twitter', 'dictionary']
    for title, website, description in objects:
        print(website)
        if len([i for i in sensitive if i in website]):
            continue
        elif 'www.' in website:
            data = DataTable.objects.filter(website__icontains=website.split('www.')[1].split('/')[0], kw_id=kwid)
            if data:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                continue
            else:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': None}]
                DataTable.objects.create(title=title, website=website, description=description,
                                         creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
        elif 'http' in website:
            # print(website.split('://')[1].split('/')[0])
            data = DataTable.objects.filter(website__icontains=website.split('://')[1].split('/')[0], kw_id=kwid)
            if data:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                continue
            else:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': None}]
                DataTable.objects.create(title=title, website=website, description=description,
                                         creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
        else:
            # print(website.split('/')[0])
            data = DataTable.objects.filter(website__icontains=website.split('/')[0], kw_id=kwid)
            if data:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                continue
            else:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': None}]
                DataTable.objects.create(title=title, website=website, description=description,
                                         creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
    return datad


def askinfo(kw, pagenum, kwid):
    ask(kw, str(pagenum), kwid)
    dbkw = KeywordTable.objects.get(keyword__iexact=kw)
    dbkw.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    dbkw.save()


# Bing获取到的信息——————————————————————————————————————————————————————————————————————————————————————
class bing():
    def __init__(self, kwlist, pagenum, kwid):
        self.url = 'https://cn.bing.com/search?q={}&first={}&ensearch=1'
        self.kwlist = kwlist
        self.pagenum = pagenum
        self.kwid = kwid
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
            self.trueurl = self.url.format(kw + 'Co.'.replace(' ', '+'), '{}')
            print('-----------------', self.trueurl)
            # print(self.trueurl)
            yield self.trueurl

    def getresult(self):
        kwurls = self.__gettrueurl()  # 替换成关键字的URL迭代器
        for kwurl in kwurls:  # 关键字加上页码
            print(kwurl)
            perpageurl = kwurl.format(str((self.pagenum - 1) * 14))
            # print(perpageurl)
            resp = r.get(perpageurl, headers=self.headers, proxies=proxies_data)
            # print(resp.text)
            # with open('bing.html', 'w') as f:
            #     f.write(resp.text)
            #     f.close()
            # print(resp.text)
            e = etree.HTML(resp.text)
            logo_items = e.xpath('//ol[@id="b_results"]/li[@class="b_algo"]')

            if not logo_items:
                resp = r.get(perpageurl, headers=self.headers, proxies=proxies_home)
                e = etree.HTML(resp.text)
                logo_items = e.xpath('//ol[@id="b_results"]/li[@class="b_algo"]')
                if not logo_items:
                    resp = r.get(perpageurl, headers=self.headers, proxies=proxies_google_search)
                    e = etree.HTML(resp.text)
                    logo_items = e.xpath('//ol[@id="b_results"]/li[@class="b_algo"]')

            elememtscount = len(logo_items)



            datad = []
            sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                         'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook',
                         'twitter', 'dictionary']
            for count in range(1, elememtscount + 1):
                title = e.xpath('string(//ol[@id="b_results"]/li[@class="b_algo"][{}]/h2/a)'.format(str(count)))
                website = e.xpath(
                    'string(//ol[@id="b_results"]/li[@class="b_algo"][{}]/h2/a/@href)'.format(str(count)))
                print(website)
                if len([i for i in sensitive if i in website]):
                    continue
                description = e.xpath(
                    'string(//ol[@id="b_results"]/li[@class="b_algo"][{}]/div/p)'.format(str(count)))
                if 'www.' in website:
                    # print(website.split('www.')[1].split('/')[0])
                    data = DataTable.objects.filter(website__icontains=website.split('www.')[1].split('/')[0],
                                                    kw_id=self.kwid)
                    if data:
                        datad += [
                            {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                        continue
                    else:
                        datad += [
                            {'title': title, 'website': website, 'description': description, 'mail': None}]
                        DataTable.objects.create(title=title, website=website, description=description,
                                                 creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 kw_id=self.kwid)
                elif 'http' in website:
                    # print(website.split('//')[1].split('/')[0])
                    data = DataTable.objects.filter(website__icontains=website.split('//')[1].split('/')[0],
                                                    kw_id=self.kwid)
                    if data:
                        datad += [
                            {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                        continue
                    else:
                        datad += [
                            {'title': title, 'website': website, 'description': description, 'mail': None}]
                        DataTable.objects.create(title=title, website=website, description=description,
                                                 creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 kw_id=self.kwid)
                else:
                    # print(website.split('/')[0])
                    data = DataTable.objects.filter(website__icontains=website.split('/')[0], kw_id=self.kwid)
                    if data:
                        datad += [
                            {'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                        continue
                    else:
                        datad += [
                            {'title': title, 'website': website, 'description': description, 'mail': None}]
                        DataTable.objects.create(title=title, website=website, description=description,
                                                 creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                 kw_id=self.kwid)
            dbkw = KeywordTable.objects.get(pk=self.kwid)
            dbkw.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            dbkw.save()
            return datad


def binginfo(kwid, pagenum, *args):
    b = bing(args, pagenum, kwid)  # bing对象
    print(b.kwlist, b.kwid, b.pagenum)
    bingData = b.getresult()
    return bingData


def getNaver(kw, start, kwid):
    url = 'https://search.naver.com/search.naver?query={}&start={}&where=webkr'.format(kw + 'Co.', start)
    resp = r.get(url=url, proxies=proxies_data)
    # print(resp.text)
    # with open('naver.html', 'wb') as f:
    #     f.write(resp.content)
    e = etree.HTML(resp.text)
    titles = []
    descriptions = []
    for i in range(10):
        title = e.xpath('string(//ul[@id="elThumbnailResultArea"]/li[{}]/dl/dt/a)'.format(str(i + 1)))
        titles.append(title)
        description = e.xpath(
            'string(//ul[@id="elThumbnailResultArea"]/li[{}]/dl/dd[@class="sh_web_passage"])'.format(str(i + 1)))
        descriptions.append(description)
    print(len(titles), len(descriptions))
    websites = e.xpath('//ul[@id="elThumbnailResultArea"]/li/dl/dd[1]/div/a/@href')
    objects = zip(titles, websites, descriptions)
    datad = []
    sensitive = ['overstock', 'amazon', 'ebay', 'alibaba', 'youtube', 'microsoft', 'twitter', 'google', 'baidu',
                 'qq', 'weixin', 'wechat', 'tencent', '%', 'linkedin', 'wikipedia', 'github', 'facebook',
                 'twitter', 'dictionary', 'sara', 'pdf']
    for title, website, description in objects:
        if len([i for i in sensitive if i in website]):
            continue
        elif 'www.' in website:
            data = DataTable.objects.filter(website=website, kw_id=kwid)
            if data:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                continue
            else:
                try:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    datad += [{'title': title, 'website': website, 'description': description, 'mail': None}]
                except:
                    pass
        elif 'http' in website:
            # print(website.split('://')[1].split('/')[0])
            data = DataTable.objects.filter(website=website, kw_id=kwid)
            if data:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                continue
            else:
                try:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    datad += [{'title': title, 'website': website, 'description': description, 'mail': None}]
                except:
                    pass
        else:
            # print(website.split('/')[0])
            data = DataTable.objects.filter(website=website, kw_id=kwid)
            if data:
                datad += [{'title': title, 'website': website, 'description': description, 'mail': data[0].mail}]
                continue
            else:
                try:
                    DataTable.objects.create(title=title, website=website, description=description,
                                             creattime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), kw_id=kwid)
                    datad += [{'title': title, 'website': website, 'description': description, 'mail': None}]
                except:
                    pass
    return datad


# 获得到的邮箱——————————————————————————————————————————————————








def googlemail(kw):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
    }
    mailstart = 0

    # 2021.2.26 更改

    print('即将爬取谷歌邮箱')
    while mailstart <= 20:
        print(mailstart)
        searchurl = 'http://www.google.com.hk/search?q={}&start={}'.format(kw, mailstart)
        # proxies = random.choice(proxy_list)
        # resp = r.get(searchurl, proxies=proxies_google_search)

        pro_list = [(proxies_data1, '数据中心1'), (proxies_data2, '数据中心2')]
        proo_list = random.choices(pro_list,k=2)
        proxy_list = proo_list + [
                      (proxies_home, "动态住宅"), (proxies_google_search, "搜索引擎"), ({}, '无')]
        # print(proxy_list)

        resp_text = ""
        block_list = []
        for proxies in proxy_list:
            resp = r.get(searchurl, proxies=proxies[0], headers={"User-Agent": random.choice(headers_li), })
            e = etree.HTML(resp.text)
            block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
            # block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
            if block_list:
                # with open('111.html','wb') as f:
                #     f.write(resp.content)
                print('爬虫获得结果，用到代理为：%s' % proxies[1])
                resp_text =  resp.text
                break



        # resp = r.get(searchurl, proxies=proxies_data1, headers={"User-Agent": random.choice(headers_li), })
        # e = etree.HTML(resp.text)
        # block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        # print('*-'*50)
        # if not block_list:
        #     print('数据中心代理1失败')
        #     resp = r.get(searchurl, proxies=proxies_data2, headers={"User-Agent": random.choice(headers_li), })
        #     e = etree.HTML(resp.text)
        #     block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        #     if not block_list:
        #         print('数据中心代理2失败')
        #         resp = r.get(searchurl, proxies=proxies_home,headers={"User-Agent": random.choice(headers_li),})
        #         e = etree.HTML(resp.text)
        #         block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        #         if not block_list:
        #             print("住宅失败")
        #             resp = r.get(searchurl, proxies=proxies_google_search, headers={"User-Agent": random.choice(headers_li),})
        #             e = etree.HTML(resp.text)
        #             block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        #             if not block_list:
        #                 print('搜索引擎失败')
        #                 break
        # resp = r.get(searchurl, proxies={})
        # with open('mail.html', 'wb') as f:
        #     f.write(resp.content)
        #     f.close()
        # if 'did not match any documents' not in resp.text:  # 说明有内容
        print('*-' * 50)
        if '找不到和您查询' not in resp_text:  # 说明有内容
            ts = resp_text
            rule = re.compile('([_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,}))')
            result = rule.findall(ts)
            mailstart += 10

            # 添加如下
            emails = [i[0] for i in result if "xx@xx" not in i[0] and not is_pic(i[0])]

            yield emails
        else:
            break

    '''
        while mailstart <= 20:
        print(mailstart)
        searchurl = "https://www.bing.com/search?q={}&first={}&count=10".format(kw, mailstart)
        resp = r.get(searchurl, proxies=proxies_data,headers=headers)
        e = etree.HTML(resp.text)
        block_list = e.xpath("//li[@class='b_algo']")
        if not block_list:
            resp = r.get(searchurl, proxies=proxies_home, headers=headers)
            e = etree.HTML(resp.text)
            block_list = e.xpath("//li[@class='b_algo']")
            if not block_list:
                resp = r.get(searchurl, proxies=proxies_google_search, headers=headers)
                e = etree.HTML(resp.text)
                block_list = e.xpath("//li[@class='b_algo']")
        # resp = r.get(searchurl, proxies={})
        # with open('mail.html', 'wb') as f:
        #     f.write(resp.content)
        #     f.close()
        # if 'did not match any documents' not in resp.text:  # 说明有内容
        if '找不到和您查询' not in resp.text:  # 说明有内容
            ts = resp.text
            rule = re.compile('([a-zA-Z1-9_-]+@\w+\.\w{3,6})')
            result = rule.findall(ts)
            mailstart += 10

            # 添加如下
            li = []
            for i in result:
                if "xx@xx" not in i:
                    li.append(i)
            yield li

            # yield result
        else:
            break
    '''


def googlemail2(kw):
    headers = {
        # "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
    }
    mailstart = 0
    mails = []

    while mailstart <= 20:
        print(mailstart)
        searchurl = "https://www.bing.com/search?q={}&first={}&count=10".format(kw, mailstart)
        resp = r.get(searchurl, proxies=proxies_data, headers=total_headers)
        e = etree.HTML(resp.text)
        block_list = e.xpath("//li[@class='b_algo']")
        if not block_list:
            resp = r.get(searchurl, proxies=proxies_home, headers=total_headers)
            e = etree.HTML(resp.text)
            block_list = e.xpath("//li[@class='b_algo']")
            if not block_list:
                resp = r.get(searchurl, proxies=proxies_google_search, headers=total_headers)
                e = etree.HTML(resp.text)
                block_list = e.xpath("//li[@class='b_algo']")
        # resp = r.get(searchurl, proxies={})
        # with open('mail.html', 'wb') as f:
        #     f.write(resp.content)
        #     f.close()
        # if 'did not match any documents' not in resp.text:  # 说明有内容
        if '找不到和您查询' not in resp.text:  # 说明有内容
            ts = resp.text
            rule = re.compile('([a-zA-Z1-9_-]+@\w+\.\w{3,6})')
            result = rule.findall(ts)
            mailstart += 10

            # 添加如下
            # li = []
            for i in result:
                if "xx@xx" not in i:
                    # li.append(i)
                    mails.append(i)
            # yield li

            # yield result
        else:
            break
    return mails

    '''
        while mailstart <= 20:
        print(mailstart)
        searchurl = 'http://www.google.com.hk/search?q={}&start={}'.format(kw, mailstart)
        proxies = random.choice(proxy_list)
        # resp = r.get(searchurl, proxies=proxies_google_search)

        resp = r.get(searchurl, proxies=proxies_home, headers=headers)
        e = etree.HTML(resp.text)
        block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
        if not block_list:
            resp = r.get(searchurl, proxies=proxies_google_search, headers=headers)
            e = etree.HTML(resp.text)
            block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
            if not block_list:
                break
        # resp = r.get(searchurl, proxies={})
        # with open('mail.html', 'wb') as f:
        #     f.write(resp.content)
        #     f.close()
        # if 'did not match any documents' not in resp.text:  # 说明有内容
        if '找不到和您查询' not in resp.text:  # 说明有内容
            ts = resp.text
            rule = re.compile('([a-zA-Z1-9_-]+@\w+\.\w{3,6})')
            result = rule.findall(ts)
            mailstart += 10
            # li = []
            for i in result:
                if "xx@xx" not in i:
                    # li.append(i)
                    mails.append(i)
            # yield li

            # yield result
        else:
            break
    return mails
    '''

    '''
    
    while mailstart <= 20:
        print(mailstart)
        searchurl = "https://www.bing.com/search?q={}&first={}&count=10".format(kw, mailstart)
        resp = r.get(searchurl, proxies=proxies_data,headers=headers)
        e = etree.HTML(resp.text)
        block_list = e.xpath("//li[@class='b_algo']")
        if not block_list:
            resp = r.get(searchurl, proxies=proxies_home, headers=headers)
            e = etree.HTML(resp.text)
            block_list = e.xpath("//li[@class='b_algo']")
            if not block_list:
                resp = r.get(searchurl, proxies=proxies_google_search, headers=headers)
                e = etree.HTML(resp.text)
                block_list = e.xpath("//li[@class='b_algo']")
        # resp = r.get(searchurl, proxies={})
        # with open('mail.html', 'wb') as f:
        #     f.write(resp.content)
        #     f.close()
        # if 'did not match any documents' not in resp.text:  # 说明有内容
        if '找不到和您查询' not in resp.text:  # 说明有内容
            ts = resp.text
            rule = re.compile('([a-zA-Z1-9_-]+@\w+\.\w{3,6})')
            result = rule.findall(ts)
            mailstart += 10

            # 添加如下
            # li = []
            for i in result:
                if "xx@xx" not in i:
                    # li.append(i)
                    mails.append(i)
            # yield li

            # yield result
        else:
            break
    return mails
    '''


def gettruest(mails):
    # [[[],[],[],[],],[],[]]
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


# 将数据库中某个关键字sofa 对应的所有数据中没有邮箱的， 全部爬取邮箱
def getmail(kwid):  # 拿刚取到的网址来抽取邮箱
    print('进入获取邮箱', kwid)
    allnone = DataTable.objects.filter(kw_id=kwid, mail=None)
    print(len(allnone))
    for eachnone in allnone:
        website = eachnone.website
        if 'www.' in website:
            newsite = website.split('www.')[1].split('/')[0]
        elif 'http' in website:
            newsite = website.split('://')[1].split('/')[0]
        else:
            newsite = website.split('/')[0]
        newsite = 'mail+@+' + newsite
        mails = googlemail(newsite)
        maildata = ';'.join(gettruest(mails))
        if len(maildata) > 5:
            eachnone.mail = maildata
            eachnone.creattime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # ###########//
            eachnone.save()
        else:
            continue


# 抓取网站信息必要关键词为engine，kw， num。
# 根据关键字，引擎 页码 搜索数据，num=0，默认数据库查找。 num=1，即时 爬虫某搜素引擎 第一页数据！
def getweb(request):
    '''
    类似 tradeinfo（所有搜索引擎都查找），只不过这里是指定搜索引擎，
    :param request:
    :return:
    '''
    time1 = time.time()
    searchEngine = request.GET.get('engine')
    kw = request.GET.get('kw')  # 关键字
    pagenum = int(request.GET.get('num', 0))  # 具体页数
    print(kw, pagenum)
    dbkw = KeywordTable.objects.filter(keyword=kw)  # 模糊查询
    if len(dbkw) == 0:
        if pagenum == 0:
            return HttpResponse('数据库中无该字段')
        KeywordTable.objects.create(keyword=kw, googleind=1, askind=1, bingind=1,
                                    updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    kwid = KeywordTable.objects.get(keyword=kw).id
    # pagenum = 0 , 从数据库里面查询 结果并返回
    # 否则，去谷歌爬取新数据，保存数据库  并返回结果
    if pagenum == 0:
        results = DataTable.objects.filter(kw_id=kwid)
        return render(request, 'result.html', {'res': results})
    pagenum -= 1
    if searchEngine == 'google':
        result = googleinfo(kw, kwid, pagenum)
    elif searchEngine == 'bing':
        result = binginfo(kwid, pagenum, kw)
    elif searchEngine == 'ask':
        result = ask(kw, pagenum, kwid)
    elif searchEngine == 'yahoo':
        result = yahoo(kw, pagenum, kwid)
    elif searchEngine == 'naver':
        result = getNaver(kw, pagenum, kwid)
    else:
        return HttpResponse('搜索引擎不正确')
    # result = DataTable.objects.filter(kw_id=kwid).order_by('-creattime')
    print('运行时间:', time.time() - time1)

    return render(request, 'result.html', {'res': result})
    # res = {
    #     "data":result
    # }
    # return JsonResponse(res)


def test(request):
    url = "http://www.google.com"
    try:
        proxies = random.choice(proxy_list)
        ret = request.get(url, proxies=proxies)
        msg = 'ok'
    except Exception as e:
        print(e)
        msg = 'error'
    return HttpResponse(msg)


def get_web(request):
    '''
       类似 tradeinfo（所有搜索引擎都查找），只不过这里是指定搜索引擎，
       :param request:
       :return:
       '''
    print('/*****************')
    time1 = time.time()
    searchEngine = request.GET.get('engine')
    kw = request.GET.get('kw')  # 关键字
    pagenum = int(request.GET.get('num', 0))  # 具体页数
    print(kw, pagenum)
    dbkw = KeywordTable.objects.filter(keyword=kw)  # 模糊查询
    if len(dbkw) == 0:
        if pagenum == 0:
            return HttpResponse('no data')
        KeywordTable.objects.create(keyword=kw, googleind=1, askind=1, bingind=1,
                                    updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    kwid = KeywordTable.objects.get(keyword=kw).id
    # pagenum = 0 , 从数据库里面查询 结果并返回
    # 否则，去谷歌爬取新数据，保存数据库  并返回结果
    if pagenum == 0:
        results = DataTable.objects.filter(kw_id=kwid)
        res = serializers.serialize('json', results)
        return HttpResponse(res)
    pagenum -= 1
    if searchEngine == 'google':
        result = googleinfo(kw, kwid, pagenum)
    elif searchEngine == 'bing':
        result = binginfo(kwid, pagenum, kw)
    elif searchEngine == 'ask':
        result = ask(kw, pagenum, kwid)
    elif searchEngine == 'yahoo':
        result = yahoo(kw, pagenum, kwid)
    elif searchEngine == 'naver':
        result = getNaver(kw, pagenum, kwid)
    else:
        return HttpResponse('engine error')
    # result = DataTable.objects.filter(kw_id=kwid).order_by('-creattime')
    print('运行时间:', time.time() - time1)

    # return render(request, 'result.html', {'res': result})
    res = {
        "data": result
    }

    return JsonResponse(res)


def get_web_new(request):
    '''
       类似 tradeinfo（所有搜索引擎都查找），只不过这里是指定搜索引擎，和上边比 不在保存数据库！！
       :param request:
       :return:
       '''
    searchEngine = request.GET.get('engine')
    kw = request.GET.get('kw')  # 关键字
    num = int(request.GET.get('num', 1))  # 具体页数
    result = new_googleinfo(kw, num)

    print(len(result))
    res = {
        "data": result
    }
    return JsonResponse(res)


def getyahoo(request):
    time1 = time.time()
    kw = request.GET.get('kw')  # 关键字
    pagenum = int(request.GET.get('num'))  # 具体页数
    print(kw, pagenum)
    dbkw = KeywordTable.objects.filter(keyword__iexact=kw)  # 模糊查询
    if len(dbkw) == 0:
        if pagenum == 0:
            return HttpResponse('数据库中无该字段')
        KeywordTable.objects.create(keyword=kw, googleind=1, askind=1, bingind=1,
                                    updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    kwid = KeywordTable.objects.get(keyword=kw).id
    if pagenum == 0:
        results = DataTable.objects.filter(kw_id=kwid)
        return render(request, 'result.html', {'res': results})
    result = yahoo(kw, pagenum, kwid)
    # result = DataTable.objects.filter(kw_id=kwid).order_by('-creattime')
    print(result)
    print('运行时间:', time.time() - time1)
    return render(request, 'result.html', {'res': result})


def getAsk(request):
    time1 = time.time()
    kw = request.GET.get('kw')  # 关键字
    pagenum = int(request.GET.get('num'))  # 具体页数
    print(kw, pagenum)
    dbkw = KeywordTable.objects.filter(keyword__iexact=kw)  # 模糊查询
    if len(dbkw) == 0:
        if pagenum == 0:
            return HttpResponse('数据库中无该字段')
        KeywordTable.objects.create(keyword=kw, googleind=1, askind=1, bingind=1,
                                    updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    kwid = KeywordTable.objects.get(keyword=kw).id
    if pagenum == 0:
        results = DataTable.objects.filter(kw_id=kwid)
        return render(request, 'result.html', {'res': results})
    result = ask(kw, pagenum, kwid)
    # result = DataTable.objects.filter(kw_id=kwid).order_by('-creattime')
    print(result)
    print('运行时间:', time.time() - time1)
    return render(request, 'result.html', {'res': result})


def get_mail(request):
    """
      1. 获取到的website；经过google 搜索 查询邮箱；
      2. 若未查询到邮箱，根据已查信息谷歌搜索查询其官网；
      3. 去其官网查询邮箱信息；
    :param request:
    :return:
    """
    website = request.GET.get('website')
    website = website.strip()

    if "exportersindia" in website:
        mail_data = "support@exportersindia.com;info@eilgroup.in;sumit@tcspinner.com"
        return JsonResponse({
            "mail": mail_data,
        })

    if 'www.' in website:
        newsite = website.split('www.')[1].split('/')[0]
    elif 'http' in website:
        newsite = website.split('://')[1].split('/')[0]
    else:
        newsite = website.split('/')[0]
    newsite = 'mail+@+' + newsite
    mails = googlemail(newsite)
    maildata = ';'.join(gettruest(mails))
    return JsonResponse({
        "mail": maildata,
    })


def getnewmail(request):
    '''
     url中携带一个website。数据库中有该网站对应的域名，就找到该记录，返回邮箱（没有就重新爬虫获取一次！！！）
    :param request:
    :return:
    '''
    website = request.GET.get('website')
    print(website)
    if ' ' in website:
        website = website.split(' ')[0]
        print(website)
    print('++++++++++')
    data = DataTable.objects.filter(website__icontains=website)
    if data:
        # 当数据库中有多个包含该website对应域名的时候，取数据库中的第一条记录！
        data = data[0]
    else:
        return HttpResponse("数据库中无此网站！")

    if data.mail == None:
        if 'www.' in website:
            newsite = website.split('www.')[1].split('/')[0]
        elif 'http' in website:
            newsite = website.split('://')[1].split('/')[0]
        else:
            newsite = website.split('/')[0]
        newsite = 'mail+@+' + newsite
        mails = googlemail(newsite)
        maildata = ';'.join(gettruest(mails))
        # DataTable.objects.get(website=website)
        if len(maildata) > 5:
            data.mail = maildata
            data.creattime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # ###########//
            key = KeywordTable.objects.get(pk=data.kw_id)
            key.updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            data.save()
            key.save()
        return HttpResponse(data.mail)
    else:
        return HttpResponse(data.mail)


def tradeinfo(request):
    '''
    1.关键字+页码查询。（数据库查询+搜索引擎查询）
    关键词如果不在数据库，那么添加至key-table，并立马执行谷歌、ask、bing等引擎搜索，搜出对应的网站，并将（网站标题、描述、网址）添加至数据库 data-table！！！
        然后执行邮箱查询，将该关键字对应的所有data-table中的数据（邮箱为空）搜寻邮箱，并保存数据库！！！
    关键词如果在数据库，如果num为0 ，直接将数据库中所有的数据查询出！
                    如果num不为0，通过搜索引擎查找对应页码的网站信息。如果刚查出的信息已经在数据库中存在，那么不需要再次保存至数据库，反之，保存！
    :param request:
    :return:
    '''
    # print(request.POST)
    time1 = time.time()
    kw = request.POST.get('kw')  # 关键字
    pagenum = int(request.POST.get('num'))  # 具体页数
    print(kw, pagenum)
    dbkw = KeywordTable.objects.filter(keyword__iexact=kw)  # 模糊查询
    if len(dbkw) == 0:
        if pagenum == 0:
            return HttpResponse('数据库中无该字段')
        KeywordTable.objects.create(keyword=kw, googleind=1, askind=1, bingind=1,
                                    updatetime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    kwid = KeywordTable.objects.get(keyword=kw).id
    if pagenum == 0:
        results = DataTable.objects.filter(kw_id=kwid)
        return render(request, 'result.html', {'res': results})
    googleinfo(kw, kwid, pagenum)
    askinfo(kw, pagenum, kwid)
    binginfo(kwid, pagenum, kw)
    getmail(kwid)  # 解析网站获得邮箱
    results = DataTable.objects.filter(kw_id=kwid, mail__isnull=False).order_by('-creattime')
    print(time.time() - time1)
    return render(request, 'result.html', {'res': results})


def searchweb(request):
    website = request.GET.get('website')
    data = DataTable.objects.filter(website__icontains=website)
    print(data)
    return HttpResponse(data)


def getemail_from_keyid(request):
    '''
    查询某个关键词对应数据库中mail为none的数据，然后查询邮箱并更新保存！
    :param request:
    :return:
    '''
    kid = request.GET.get('kid')
    getmail(int(kid))
    return HttpResponse(1)
