import random
from lxml import etree
import requests
headers = {
    "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}

headers_li = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36",
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400',

]
proxies_home = {
    'http': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-sstrade-zone-residential-country-us:Shengshikeji666@zproxy.lum-superproxy.io:22225'
}

url = "http://www.google.com/search?q={}".format("sofa")

proxies = {}
response = requests.get(url, headers={"User-Agent": headers_li[0], }, proxies=proxies)
with open('proxy_test.html','wb') as f:
    f.write(response.content)
e = etree.HTML(response.text)
block_list = e.xpath("//div[@class='g Ww4FFb vt6azd tF2Cxc']")
print(len(block_list))
if not block_list:
    print(1)

