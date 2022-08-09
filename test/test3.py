import requests
from lxml import etree

proxies = {
'http': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225'
}
proxies = {}
url = "http://www.google.com/search?q=sofa&start=0"
# url = "http://www.google.com.hk/search?q=sofa"
ret = requests.get(url,proxies=proxies)
# print(ret.text)
with open('google444.html', 'wb') as f:
    f.write(ret.content)
e = etree.HTML(ret.text)
block_list = e.xpath("//div[@class='g Ww4FFb vt6azd tF2Cxc']")
print(len(block_list))
res_list = []
for block in block_list[0:5]:
    title = block.xpath('.//h3/span/text()')
    print(title)
    website = block.xpath('.//div/div/a/@href')
    description = block.xpath('string(.//div/div[2]/div/span)')
    title = title[0] if title else ""
    website = website[0] if website else ""
    s = (title, website, description)
    res_list.append(s)
print(res_list)