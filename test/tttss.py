from lxml import etree
import requests as r
import random
keyword = 'sofa'
cont = ''
user_agent_li = []
proxies_home = {
    'http': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225'
}
# 1.印度b2b 搜索  返回结果数量！！
url = 'https://www.exportersindia.com/search.php?srch_catg_ty=prod&term={}&cont={}'
url = url.format(keyword, cont)
headers = {
   # "User-Agent": random.choice(user_agent_li),
    # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
ret = r.get(url, headers=headers, proxies=proxies_home)
e = etree.HTML(ret.content.decode('utf-8'))
num1 = e.xpath('//span[@class="large"]/text()')[0] if e.xpath('//span[@class="large"]/text()') else 0
num1 = int(num1)
print("印度的b2b数量：", num1)
