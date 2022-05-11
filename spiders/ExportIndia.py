import requests
from lxml import etree
import json
import threading
import random
from django.db import connections
from .user_agent_list import user_agent_li

'''
1.关键词 + 页码 + 国家代码 发送url请求
2.解析页面  获取公司名  和   网址
          网址分两种：
                1.站内网站【无法得到邮箱等信息，待进一步处理】  ---https://www.exportersindia.com/syed-khaleel-furniture/
                2.该公司的官网）
2.1
    对于站内网站，提取其 公司名 + 详细地理位置  ， 调用谷歌地图搜索  查询其信息，如website 官网、 phone等！！
3.调用接口查询邮箱手机号等信息（将website作为参数传递，去官网页面查询邮箱    或   去联系我们对应的页面中查询  如包含 contact 、 service、customer 的a标签）



'''

'''
https://www.exportersindia.com/search.php?srch_catg_ty=prod&term=led&cont=IN&pageno=1
https://www.exportersindia.com/search.php?srch_catg_ty=prod&term=led&cont=IN&pageno=2
'''

'''
印度 ； IN
马来西亚：MY
菲律宾：PH
泰国：TH
越南：VN
老挝：LA
柬埔寨：KH
缅甸：MM
文莱：BN
新加坡：SG
印度尼西亚：ID
东帝汶：TL
'''

proxies_data2 =  {'http': 'http://lum-customer-hl_60c2da6c-zone-data_center:fms4eky4mb70@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_60c2da6c-zone-data_center:fms4eky4mb70@zproxy.lum-superproxy.io:22225'}

proxies_data1 = {'http': 'http://lum-customer-hl_60c2da6c-zone-zone1:qx6l05p8ekj5@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_60c2da6c-zone-zone1:qx6l05p8ekj5@zproxy.lum-superproxy.io:22225'}

proxies_data = random.choice([proxies_data1, proxies_data2])
proxies_home = proxies_data
# proxies_home = {
# }
#
# proxies_google_search = {
# }
headers_li = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',

]
total_headers = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
}



def Spider_detail_eu(second_url, headers, proxies, li, company,country,description):
    print(second_url)
    second_ret = requests.get(second_url, headers=total_headers, proxies=proxies)

    e2 = etree.HTML(second_ret.content)
    addr = e2.xpath('string(//dd[@itemprop="addressLocality"])')
    phone = e2.xpath('string(//a[@class="stickybar-button js-click-tel"])')
    website = e2.xpath('//a[@class="page-action"]/@href')

    phone = phone.replace(" ", "").replace("Call", "").strip() if phone else ""
    website = website[0].strip() if website else ""


    di2 = {}
    di2["company"] = company
    di2["address"] = addr
    di2["phone"] = phone
    di2["website"] = website
    di2["description"] = description
    di2["country"] = country
    li.append(di2)

def Spider_detail(second_url, total_headers, proxies, li, company):
    print(second_url)
    second_ret = requests.get(second_url, headers=total_headers, proxies=proxies)
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
    address = di.get("Address", "")
    landline = di.get("Landline", "")
    mobile = di.get("Mobile", "")
    phone = landline + ";" + mobile
    phone = phone.strip().strip(";")
    email = di.get("Email", "")
    website = di.get("Website", "")
    if website:
        if "+86" in phone.replace(" ", ""):
            pass
        elif "china" in address.replace(" ", ""):
            pass
        elif "china" in website.replace(" ", ""):
            pass
        elif "china" in company.replace(" ", ""):
            pass
        elif "@edu" in email.replace(" ", ""):
            pass
        elif "@gov" in email.replace(" ", ""):
            pass
        else:
            di2 = {}
            di2["company"] = company
            di2["address"] = address
            di2["phone"] = phone
            di2["email"] = email if email else ""
            di2["website"] = website
            li.append(di2)


def export_europages(keyword, pagenum):
    proxies = proxies_data
    ua = random.choice(user_agent_li)
    headers = {
        "User-Agent": ua,
    }
    url = "https://www.europages.co.uk/companies/pg-{}/{}.html".format(pagenum, keyword)

    ret = requests.get(url=url, headers=total_headers, proxies=proxies)
    e = etree.HTML(ret.content)

    block_list = e.xpath("//li[@class='article-company card card--1dp vcard']")
    li = []
    threads = []
    for block in block_list:
        company = block.xpath('.//div[@class="company-info"]/a/text()')
        country = block.xpath('.//div[@class="company-info"]/div/div/span[2]/text()')
        description = block.xpath('.//p[@class="company-description"]/text()')
        page_href = block.xpath('.//div[@class="company-info"]/a/@href')
        country = country[0].strip().upper() if country else ""
        if country == 'CHINA':
            print('此项为中国商家，过滤！')
            continue
        company = company[0].strip() if company else ""
        description = description[0].strip() if description else ""
        page_href = page_href[0].strip() if page_href else ""

        t = threading.Thread(target=Spider_detail_eu, args=(page_href, headers, proxies, li, company,country,description))
        threads.append(t)
        t.start()

    # 等待所有线程任务结束。
    for t in threads:
        t.join()
    return li

def export_yellowpages_ph(keyword, pagenum):
    proxies = proxies_data
    ua = random.choice(user_agent_li)
    headers = {
        "User-Agent": ua,
    }

    url = "https://www.yellow-pages.ph/search/{}/nationwide/page-{}".format(keyword, pagenum)
    ret = requests.get(url=url, headers=total_headers, proxies=proxies)

    e = etree.HTML(ret.content.decode())

    block_list = e.xpath('//div[@class="search-listing"]')
    pagenum = int(pagenum)
    if pagenum > 1:
        block_list = block_list[1:]
    li = []
    threads = []
    for block in block_list:
        company = block.xpath('.//h2[@class="search-tradename"]/a/text()')[0]
        second_url = "https://www.yellow-pages.ph" + block.xpath('.//h2[@class="search-tradename"]/a/@href')[0]

        t = threading.Thread(target=Spider_detail, args=(second_url, headers, proxies, li, company))
        threads.append(t)
        t.start()

    # 等待所有线程任务结束。
    for t in threads:
        t.join()
    return li


def export_india_spider(keyword, pageno, cont):
    url = 'https://www.exportersindia.com/search.php?srch_catg_ty=prod&term={}&cont={}&pageno={}'
    # keyword = 'sofa'
    url = url.format(keyword, cont, pageno)
    print(url)
    headers = {
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        "User-Agent": random.choice(user_agent_li),
    }

    ret = requests.get(url, headers=total_headers, proxies=proxies_data)
    e = etree.HTML(ret.text)
    total_count = e.xpath('//span[@class="large"]/text()')[0] if e.xpath('//span[@class="large"]/text()') else 0
    item_list = e.xpath(
        "//div[@id='classified_grid_wrap']/ul/li[@class='fo classified with_thumb big_text']/div[@class='class_address']")
    if not item_list:
        ret = requests.get(url, headers=total_headers, proxies=proxies_home)
        e = etree.HTML(ret.text)
        total_count = e.xpath('//span[@class="large"]/text()')[0] if e.xpath('//span[@class="large"]/text()') else 0
        item_list = e.xpath(
            "//div[@id='classified_grid_wrap']/ul/li[@class='fo classified with_thumb big_text']/div[@class='class_address']")
    print(len(item_list))

    data_list = []
    thread_list = []
    cursor = connections['trade'].cursor()
    for item in item_list:
        company = item.xpath(".//p[1]/a[1]/text()")[0] if item.xpath(".//a[1]/text()") else ""
        #website = item.xpath(".//p[1]/a[1]/@onclick")[0] if item.xpath(".//a[1]/@onclick") else ""
        #website = website.split("(")[1].split(',')[0][1:-1] if website else ""
        website = item.xpath(".//p[1]/a[1]/@href")[0]
        if "javascript" in website:
        	continue
        addr = item.xpath(".//p[2]/text()")[0].strip()[0:-1] if item.xpath(".//p[2]/text()") else ""
        print('----------------------')
        print(company)
        print('----------------------')
        s = ""
        try:
            s = website + company + addr
        except Exception as e:
            print(e)

        if 'china' in s.lower() or 'alibaba' in s.lower():
            continue

        # 如果查询的数据 有website，直接返回数据
        if website:
            di = {}
            di["company"] = company
            di["website"] = website
            di["addr"] = addr
            di["phone"] = ""
            data_list.append(di)
            continue

        # 如果查询的数据 没有website，那么先从数据库查询
        else:
            cursor.execute("select * from search_result where company=%s",[company])
            ret = cursor.fetchall()
            if ret:
                ret = ret[0]
                # 从数据库中查询，如果有直接返回！
                website = ret[3]
                addr = ret[6]
                phone = ret[7]

                di = {}
                di["company"] = company
                di["website"] = website
                di["addr"] = addr
                di["phone"] = phone
                data_list.append(di)
                print("数据库查询数据并返回了。。。。。")
            else:
                # 如果没有，继续查询！
                phone = ""
                '''
                # print('1111111',website)
                # website = website if website else item.xpath(".//a[1]/@href")[0]
    
                # 2021.2.3注释下列代码
                # if not website:
                #     # 如果没有直接查询到该公司的官网，那么 通过谷歌搜索 该公司全称 来搜索其官网。
                #
                #     ret = get_website_from_google_map(company + " " + addr)
                #     if ret:
                #         website, addr, phone = ret
                '''

                # 2021.2.22修改如下代码
                # 如果没有直接查询到该公司的官网，那么 通过谷歌搜索 该公司全称 来搜索其官网。
                # t = threading.Thread(target=get_website_from_google_search_thread,args=(company,addr,data_list,headers))
                t = threading.Thread(target=get_website_from_search_engine, args=(company, addr, data_list))
                thread_list.append(t)
                t.start()
                # website = get_website_from_google_search(company,headers)

            # yield company,website,addr,phone
    cursor.close()
    for t in thread_list:
        t.join()
    print('ending............')
    return data_list


def get_website_from_search_engine(company, addr, data_list):
    # 1.先用  雅虎、ask  搜索bing 、           再用谷歌
    mapping = {
        'yahoo':search_website_by_yahoo,
        'ask':search_website_by_ask,
        'bing':search_website_by_bing,
    }

    engine_list = ['yahoo','ask','bing']
    random.shuffle(engine_list)
    website = ""
    for engine in engine_list:
        func = mapping.get(engine)
        website = func(company,proxies_data)
        if website:
           break
    if not website:
        for engine in engine_list:
            func = mapping.get(engine)
            website = func(company, proxies_home)
            if website:
                break
        if not website:
            engine = "google"
            website = search_website_by_google(company, proxies_home)
            # 5.google2
            if not website:
                engine = "google2"
                website = search_website_by_google(company, proxies_google_search)

    """
    # 1.
    engine = engine_list.pop()
    func = mapping.get(engine)
    website = func(company,proxies_data)
    # 2.
    if not website:
        engine = engine_list.pop()
        func = mapping.get(engine)
        website = func(company, proxies_data)
        # 3.
        if not website:
            engine = engine_list.pop()
            func = mapping.get(engine)
            website = func(company, proxies_data)
            # 4.google
            if not website:
                engine = "google"
                website = search_website_by_google(company, proxies_home)
                # 5.google2
                if not website:
                    engine = "google2"
                    website = search_website_by_google(company, proxies_google_search)

    """

    if not website:
        return

    if 'china' in website.lower():
        return
    else:
        # obj = models.EngineCount.objects.get(id=1)
        # if engine == 'yahoo':
        #     obj.yahoo += 1
        # elif engine == "ask":
        #     obj.ask += 1
        # elif engine == "bing":
        #     obj.bing += 1
        # elif engine == "google":
        #     obj.google += 1
        # elif engine == "google2":
        #     obj.google2 += 1
        # obj.save()

        di = {}
        di["company"] = company
        di["website"] = website
        di["addr"] = addr
        di["phone"] = ""
        data_list.append(di)

# 暂时不用
def get_website_from_google_search(company, headers):
    proxy_list = [proxies_home, proxies_home, proxies_google_search]
    proxies = random.choice(proxy_list)
    # proxies = {}
    url = "http://www.google.com/search?q={}".format(company)
    response = requests.get(url, headers=total_headers, proxies=proxies)
    e = etree.HTML(response.text)
    block_list = e.xpath('//div[@class="g"]')
    print(len(block_list))
    if not block_list:
        return ""

    for block in block_list:
        title = block.xpath('.//h3//span/text()')
        website = block.xpath('.//div/div/a/@href')
        website = website[0] if website else ""
        print(title)
        print(website)
        return website


# 暂时不用
def get_website_from_google_search_thread(company, addr, data_list, headers):
    headers = {
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
    }
    proxy_list = [proxies_home, proxies_home, proxies_google_search]
    proxies = random.choice(proxy_list)
    # proxies = {}
    url = "http://www.google.com/search?q={}".format(company)
    # response = requests.get(url,headers=headers,proxies=proxies)
    response = requests.get(url, headers=total_headers, proxies=proxies_home)
    e = etree.HTML(response.text)
    block_list = e.xpath('//div[@class="g"]')
    print(len(block_list))
    if not block_list:
        response = requests.get(url, headers=total_headers, proxies=proxies_google_search)
        e = etree.HTML(response.text)
        block_list = e.xpath('//div[@class="g"]')
        print(len(block_list))
        if not block_list:
            return ""

    # for block in block_list:
    block = block_list[0]
    title = block.xpath('.//h3//span/text()')
    website = block.xpath('.//div/div/a/@href')
    website = website[0] if website else ""

    if 'china' in website.lower():
        return
    else:
        di = {}
        di["company"] = company
        di["website"] = website
        di["addr"] = addr
        di["phone"] = ""
        data_list.append(di)
    # print(title)
    # print(website)
    # return website


def search_website_by_bing(company, proxies):
    headers = {
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        "User-Agent": random.choice(user_agent_li),
    }

    url = "https://www.bing.com/search?q={}".format(company)
    response = requests.get(url, headers=total_headers, proxies=proxies)
    with open('demo_bing.html', 'wb') as f:
        f.write(response.content)
    e = etree.HTML(response.text)
    hrefs = e.xpath("//li[@class='b_algo'][1]//h2/a/@href")
    if hrefs:
        return hrefs[0]
    else:
        return None


def search_website_by_google(company, proxies):
    headers = {
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        "User-Agent": random.choice(user_agent_li),
    }
    url = "http://www.google.com/search?q={}".format(company)
    response = requests.get(url, headers=total_headers, proxies=proxies)
    with open('demo_google.html', 'wb') as f:
        f.write(response.content)
    e = etree.HTML(response.text)
    hrefs = e.xpath('//div[@class="g"][1]//div/div/a/@href')
    if hrefs:
        return hrefs[0]
    else:
        return None


def search_website_by_yahoo(company, proxies):
    headers = {
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        "User-Agent": random.choice(user_agent_li),
    }
    url = "https://malaysia.search.yahoo.com/search?p={}".format(company)
    response = requests.get(url, headers=total_headers, proxies=proxies)
    with open('demo_yahoo.html', 'wb') as f:
        f.write(response.content)
    e = etree.HTML(response.text)
    hrefs = e.xpath('string(//div[@id="web"]/ol/li[1]/div/div/div/span[1])')
    if hrefs:
        return hrefs
    else:
        return None


def search_website_by_ask(company, proxies):
    headers = {
        "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
        "User-Agent": random.choice(user_agent_li),
    }
    url = 'https://www.ask.com/web?qo=pagination&q={}'.format(company)
    response = requests.get(url, headers=total_headers, proxies=proxies)
    with open('demo_ask.html', 'wb') as f:
        f.write(response.content)
    e = etree.HTML(response.text)
    hrefs = e.xpath('//div[@class="PartialSearchResults-item"]/div/a/@href')
    if hrefs:
        return hrefs[0]
    else:
        return None


def get_website_from_google_map(word):
    # 调用谷歌api  无需使用代理！！
    # word = "stanley lifestyles ltd Bommasandra,Bangalore, India"
    # radius = request.POST.get('radius')
    key = 'AIzaSyC2VUsehdGp0LS7uZgETWd_OoBA7DpHIYU'
    fields = 'place_id,formatted_address,name,types,geometry'
    language = 'en'
    url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?' \
          'input=%s&inputtype=textquery&key=%s&fields=%s&language=%s' % (word, key, fields, language)
    res = requests.get(url)
    json_str = res.content.decode()
    data = json.loads(json_str)

    try:
        place_id = data["candidates"][0]["place_id"]
        print(place_id)
        key = 'AIzaSyC2VUsehdGp0LS7uZgETWd_OoBA7DpHIYU'
        language = 'en'
        fields = 'formatted_address,international_phone_number,website'
        url = 'https://maps.googleapis.com/maps/api/place/details/json?place_id=%s&key=%s&language=%s&fields=%s' % (
            place_id, key, language, fields)
        res = requests.get(url)
        json_str = res.content.decode()
        data = json.loads(json_str)

        website = data["result"]["website"]
        addr = data["result"]["formatted_address"]
        phone = data["result"]["international_phone_number"]
        # print(website)
        # print(addr)
        # print(phone)
        return website, addr, phone
    except Exception as e:

        print(e, 123)
        return None

# s = export_india_spider('sofa',0,'CN',{})
# for i in s:
#     print(i)


# c = "Innova Techno Products (p) Ltd."
# get_website_from_google_search(c)
