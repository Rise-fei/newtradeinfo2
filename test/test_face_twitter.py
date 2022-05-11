import requests as r
import json
import re
from collections import Counter
from lxml import etree

headers = {
        # 'cookie': 'Internationalization=CN|CNY; OriginCountry=CN; tid=UCNzrlOL7mPT3CBNlckDKTVpQcN1zmM8yrb8z05IMWO635u9rhtDANUUinqcZoUZTxRcr8ERmIAJ10Y4_FoLQm-YTii0MyPI-7KBUcRCXHXu0DwQs7_9ZxLt-a_9lQHCbaquQw2; id=kok3zl4qnqaa135r2cmo33cu; Experience=44_A|11_A; zip=60540; zipRemember=60540; uid=6dZ-cylI8UeG46ZkVgqOrw; CBH_CRATEUS=60dvGU2f20GQuIXr5qpzRQ; AKA_A2=A; ak_bmsc=998AC6E50D94755839F099550069462E1720F8C4C40A0000FDEE7A5EC89DF93A~plydCNfTyvdPpkjUtqIh3TpDvqRyKSI1aQjlGNAUQFTtl1mj6DJcTFB815wLlgUI+eWHk3GUdM0e/1uqkCYI1ZRpcs7KFzucO6RuNNve9S9o8NZhwUb1o6JcdakQSQH9YV1LPziYNeBnSKmnNwBdz7d0hiKyQ/wMHPB6UbQv6k8FBYsMWdmgn87HAvI+eP6KC+8xaF4XPWcyYU1TrOrAso+82aNVD8PpxNFZmckoFt5wVHIS6HpTzY839jQi0RVtRG; bm_sz=4778E4CAAB1DD8117B710B5F54DC5895~YAAQxPggF0ZeXMZwAQAAmow1EAfkBSNQDU/6qlNf8QwNKsYX0EyuiD3P4+oAJwJVdp4BaL+FZPjRVDTBGNWiP5wUtbWOpgRjOFi9PR0UlUAtkXgY2TmQZYH6ukrLJW6gIq/cD0PfbARjshT0dCMvuSaofHm1fHw0KpYI+nDOTO9vT/PP7zwvW1JJpbHS80/8WCTSA7MzH10=; optimizelyEndUserId=oeu1585114883721r0.8208182152869226; ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22790da0b6-3fd0-4638-87fc-a49626673d1d%22; AMCVS_B9F81C8B5330A6F40A490D4D%40AdobeOrg=1; InternationalWelcome=1; wlcme=true; _ga=GA1.2.1037577580.1585114888; _gid=GA1.2.1407457072.1585114888; _abck=16864C232022F19D2E45962A786D0F10~0~YAAQxPggFwlfXMZwAQAAm7k1EAPIFoA1K5EpXc9izIRhkxxRrUk4yGkHSlY5S1fY9um143yytCh3AlDjArsogNeaLr2RrmZgswxReXZwNIn8oJCPXl6NGYbdtcm7854Cv64uq9Hfr334UpkMH+w7YrdTKrjwwGb3TZswrO3KV7QbQaehOrJ1qoSgnZgSj09rD1mxP/sfNQyUu7dwkVgSKH0zjbgLiw+iguuI4TaIIOpBTmatE3jisj9zx2EGS62Qah7Y1WOahmwbupPH30Bom3iTUI9Ya04lgMc5kdP/rkdaN+o17RFD2hPe53vSs9/MPHEt+sP2YzHUWxWAnveU~-1~-1~-1; basketID=227305865; basketIDRemember=227305865; hasBasket=1; s_ecid=MCMID%7C57774931402568054592901417630552029241; AMCV_B9F81C8B5330A6F40A490D4D%40AdobeOrg=-432600572%7CMCIDTS%7C18347%7CMCMID%7C57774931402568054592901417630552029241%7CMCAAMLH-1585719687%7C11%7CMCAAMB-1585719687%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1585122089s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.5.2; BrowseViewTracking=; btpdb.kbMzxFN.dGZjLjQ4OTM1NjQ=REFZUw; D_IID=2C91E143-0507-35B7-B424-2FE71E755AC7; D_UID=2494419D-F06C-3606-AC3D-F1A03213AF80; D_ZID=16717EF8-F8AD-3D61-B141-B51DC34DFB88; D_ZUID=1955B36C-F28A-3617-977C-F7FA3968FF4A; D_HID=444BA707-4174-3C7E-B2D7-74820041F05B; D_SID=119.165.240.85:teyjbEqzEBCauZE2wRqN/DohTbALerwMHMZFwt29DFQ; _gcl_au=1.1.2076564738.1585114890; QuantumMetricUserID=4f553b5e510727227706c977e8c79e20; QuantumMetricSessionID=30423bff1ea53f9c5cfb26afd5c72ff8; cbt-consent-banner=CROSS-BORDER%20Consent%20Banner; _hjid=6cdc3d5c-4850-4ed2-aa4d-e89231ad6327; __RequestVerificationToken=52q5ZZk5CbBrd2M4EFgIqwzWYboR5JtOL-HpIz8GSFN5vouUSE8v3UbHhL5gyti6GTFGKak35Kw43U-kWcPJXqGryBo1; _scid=890b5574-7eab-4f10-81c6-7662a3a3ff8d; s_pers=%20s_ev46%3D%255B%255B%2527Typed%252FBookmarked%2527%252C%25271585114889726%2527%255D%255D%7C1742881289726%3B%20gpv%3Dspill%257Cfurniture%253Aliving%2520room%2520furniture%257Csofas%2520%2526%2520loveseats%7C1585117808092%3B%20s_vs%3D1%7C1585117808108%3B%20s_nr%3D1585116008113-New%7C1616652008113%3B%20s_dl%3D1%7C1585117808116%3B; bm_sv=8DBAC03B0C1677F86F6D74A55609543D~QdU9FCQ4l0xQtkzDLFSGKQnEYWsj21lzYSp4QP4oFW4EpKOLH4RrCVknIQ0YWD7iNNdGUmvx77+SSNXjPtn3Ir4HZ+DjWOeD6bI9IdgarLELEG1h7Kb88ZTkZSANEqjlY8JU2xtZEKoySbYQPfiwl+neO6rAt45kdEnK+NuMt0E=; s_sess=%20cmgvo%3DundefinedTyped%252FBookmarkedTyped%252FBookmarkedundefined%3B%20cpcbrate%3D0%3B%20s_sq%3D%3B%20s_ppvl%3Dspill%25257Cfurniture%25253Aliving%252520room%252520furniture%25257Csofas%252520%252526%252520loveseats%252C72%252C100%252C47608%252C1300%252C875%252C1680%252C1050%252C2%252CL%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dspill%25257Cfurniture%25253Aliving%252520room%252520furniture%25257Csofas%252520%252526%252520loveseats%252C100%252C100%252C47608%252C950%252C875%252C1680%252C1050%252C2%252CL%3B; RT="z=1&dm=crateandbarrel.com&si=5eb7eddb-c45f-4e82-b88f-aee7a311b056&ss=k86wgxi7&sl=3&tt=acuk&bcn=%2F%2F684fc537.akstat.io%2F&ul=1aspo"',
        # 'cookie': 's=30423bff1ea53f9c5cfb26afd5c72ff8; U=4f553b5e510727227706c977e8c79e20',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
proxies = {}

def get_page_email(res):
    # 提取邮箱
    email_list = re.findall('([a-zA-Z1-9_-]+@\w+\.\w{3,6})', res)
    print(email_list)
    return email_list

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

def get_info_from_page(res):
    email_list = get_page_email(res)
    phone_list = get_page_phone(res)
    facebook_list = get_page_facebook(res)
    twitter_list = get_page_twitter(res)
    ret = {
        'email': email_list,
        'phone': phone_list,
        'facebook': facebook_list,
        'twitter': twitter_list,
    }

    return ret

def query_info(website):
    # 得到一个公司官网，查询官网是否有 联系信息！！！
    resp = r.get(website, headers=headers, proxies=proxies)  # 首页的响应信息
    try:
        res = resp.content.decode()
    except:
        res = resp.text
    data_dict = get_info_from_page(res)

    # 如果没有或者信息不全，爬取官网的 contact us链接 ，继续 寻找内容
    contact_us_url = ""
    resp = r.get(contact_us_url, headers=headers, proxies=proxies)  # 首页的响应信息
    try:
        res = resp.content.decode()
    except:
        res = resp.text
    data_dict = get_info_from_page(res)

    return


# ***************************************************************

def getContactWeb(u, e):
    # u = website
    #  e = etree.HTML(res)
    contact1 = e.xpath("//a[contains(text(),'contact')]/@href")
    contact2 = e.xpath("//a[contains(text(),'Contact')]/@href")
    contact = contact2 + contact1
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

