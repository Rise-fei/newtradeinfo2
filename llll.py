import random
from lxml import etree
import requests
headers = {
    "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
user_agent_li = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/531.4 (KHTML, like Gecko) Chrome/3.0.194.0 Safari/531.4',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.11 Safari/534.16',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.211.4 Safari/532.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.15) Gecko/20101027 Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/7.0.540.0 Safari/534.10',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.134 Safari/534.16']
ret = []
headers_li = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',

]
headers = {
    # "User-Agent":i,
    # "User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
      # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
}
proxies_home = {
    'http': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225'
}
proxies_data2 = {'http': 'http://lum-customer-c_0ba1644e-zone-dongnanya:01z2e4at7eps@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-c_0ba1644e-zone-dongnanya:01z2e4at7eps@zproxy.lum-superproxy.io:22225'}

url = "http://www.google.com/search?q={}".format("sofa")


response = requests.get(url, headers=headers, proxies=proxies_data2)
e = etree.HTML(response.text)
block_list = e.xpath('//div[@class="g"]')
print(len(block_list))
if not block_list:
	print("1236549790000")

# for i in headers_li:
#     proxies = proxies_data2
#     proxies = {}
#     # response = requests.get(url, headers={"User-Agent": i, }, proxies=proxies)
#     response = requests.get(url, headers=headers, proxies=proxies)
#     e = etree.HTML(response.text)
#     block_list = e.xpath('//div[@class="g"]')
#     print(len(block_list))
#     if not block_list:
#         print(i)

