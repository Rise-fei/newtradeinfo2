
from lxml import etree
import requests
headers = {
    "cookie": "CGIC=IocBdGV4dC9odG1sLGFwcGxpY2F0aW9uL3hodG1sK3htbCxhcHBsaWNhdGlvbi94bWw7cT0wLjksaW1hZ2UvYXZpZixpbWFnZS93ZWJwLGltYWdlL2FwbmcsKi8qO3E9MC44LGFwcGxpY2F0aW9uL3NpZ25lZC1leGNoYW5nZTt2PWIzO3E9MC45; CONSENT=YES+US.zh-CN+201905; HSID=ADxkA6jzRB6Pv9F4f; SSID=A6ROAQ3F_zuaK1Qwr; APISID=h4CpiJt_FUn_veK_/A7UK8BVyKyVS7O5ww; SAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; __Secure-3PAPISID=2TgO2q6ZyecVAxuJ/A8ww1CxfRa2RSfpqO; SEARCH_SAMESITE=CgQIr5EB; ANID=AHWqTUnfkyQzvSzNuYfwrEoHubemaKVuDbb3pPXl9ZvMvk4cdU0lZjX8JQz3B-Pw; SID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_L5f1FrZ-fsUuiXgitM0ItA.; __Secure-3PSID=7AfkmR-_98Dy9Ua66h8MC5c4m2GrgPCHhzE0NGMHr39ScQF_HBnPE0Oo0gUU4Ki3S52f8Q.; 1P_JAR=2021-02-23-02; UULE=a+cm9sZTogMQpwcm9kdWNlcjogMTIKdGltZXN0YW1wOiAxNjE0MDQ4NTM5MTIwMDAwCmxhdGxuZyB7CiAgbGF0aXR1ZGVfZTc6IDM0MDUyMjM0MgogIGxvbmdpdHVkZV9lNzogLTExODI0MzY4NDkKfQpyYWRpdXM6IDE3MDc1NDIwCnByb3ZlbmFuY2U6IDYK; NID=209=IjvE1SfOWSnDkdHPTmjjY_AKIQdvRZWb-TGnfJd3ELCa_xZnNiVE2NALXvzi3x6YK8arr-e6e8j_hr7VanuJq1q66cOKES0I0JgDBrWVP2Z-sQWTgef6BmDoyDdz9sh3yBpiL5vmpkDQTbjlToC5rRDmp69VU2p-pjCoLlPZtAzkdxvZKoZT7HVlybjr6mz_Wcny8KXGa-lNUABMCdjjTCNHZEosttiPKIr5CIfbg4CX_ZfuP8KQ3QwUMpV3l1W3IOMr0AHbn330bKFueuhw0SmmJE9m-b3PTkrdo4UyKWfBGYDmNu4",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"
}
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
}
proxies_data2 =  {'http': 'http://lum-customer-hl_60c2da6c-zone-data_center:fms4eky4mb70@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_60c2da6c-zone-data_center:fms4eky4mb70@zproxy.lum-superproxy.io:22225'}

proxies_data1 = {'http': 'http://lum-customer-hl_60c2da6c-zone-zone1:qx6l05p8ekj5@zproxy.lum-superproxy.io:22225',
            'https': 'http://lum-customer-hl_60c2da6c-zone-zone1:qx6l05p8ekj5@zproxy.lum-superproxy.io:22225'}



proxies_google_search = {
    'http': 'http://lum-customer-hl_60c2da6c-zone-zone2:tais4r3flqmy@zproxy.lum-superproxy.io:22225',
    'https': 'http://lum-customer-hl_60c2da6c-zone-zone2:tais4r3flqmy@zproxy.lum-superproxy.io:22225'
}
url = "http://www.google.com/search?q={}".format("sofa")
print(url)
proxies = proxies_data1
#response = requests.get(url, headers=headers,proxies=proxies_google_search)
response = requests.get(url, headers=headers,proxies=proxies)
print(response.content)
with open('aabbcc.html','wb') as f:
    f.write(response.content)

e = etree.HTML(response.text)
block_list = e.xpath("//div[@class='g Ww4FFb tF2Cxc']")
print(len(block_list))

