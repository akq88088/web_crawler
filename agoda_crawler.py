# -*- coding: utf-8 -*-
"""
@author: user
"""

import selenium
from selenium import webdriver
import time
from lxml import etree
import pandas as pd
import numpy as np

#簡化xpath指令
def get_node(node, order, index = ''):
    if index != '':
        index = str(index)
        s = "node.xpath('{}')[{}]".format(order,index)
    else:
        s = "node.xpath('{}')".format(order)
    try:
        result = eval(s)
    except:
        result = None
    return result

#開啟瀏覽器
browser = webdriver.Chrome()
website = 'https://www.agoda.com/zh-tw/pages/agoda/default/DestinationSearchResult.aspx?asq=CGrGUnvzhwxKMS%2BvfmkcHysLs8HBOYxs%2BeCgsfLhorM78hphww%2BzKZtavWFsjID9cOYN0XAVWKAVqAmoSIhTBd8kL7WEeDXmPOpAoGCaUos4%2Fvz8D%2FdoR6fQiL2VQFD%2FiOGQjCRqtvugSOJfYh77LgYr5NufC9CJdz1vLLyhtp0SvaE8g7tfsG%2B1uOMEhj%2Fbd%2BYbVu0nitcgaq4HocuVYxsFyJ6WPy9rIgk%2F4AhUbIA%3D&area=36774&cid=1744599&tick=637027815710&languageId=20&userId=49454b43-7c9b-4d3e-9ebd-3f5cdddce9cf&sessionId=rrh1hgd3dxnyvlgu4nc1lryp&pageTypeId=1&origin=TW&locale=zh-TW&tag=b869c856-8a76-7617-659b-548ba8d1ea0a&aid=82364&currencyCode=TWD&htmlLanguage=zh-tw&cultureInfoName=zh-TW&ckuid=49454b43-7c9b-4d3e-9ebd-3f5cdddce9cf&prid=0&checkIn=2019-09-09&checkOut=2019-09-10&rooms=1&adults=1&children=0&priceCur=TWD&los=1&textToSearch=%E5%8F%B0%E5%8C%97%E8%BB%8A%E7%AB%99&travellerType=0&familyMode=off&productType=-1&sort=priceLowToHigh'
browser.get(website)
for i in range(10):
    #下拉以顯示更多飯店資訊
    browser.execute_script('window.scrollBy(0,window.screen.height);')
    #等待網頁讀取資訊
    time.sleep(5)

root = etree.fromstring(browser.page_source, etree.HTMLParser())
log_dict = {"title":[], "star":[], "location":[], "adv":[], "coupon":[], "score":[], "price_pre":[],
            "price_after":[], "recommend":[], "crawler_time":[]}
iRun = 1
#走訪儲存每個飯店的li節點
for room in root.xpath('//li[@data-selenium = "hotel-item"]'):
    if iRun % 10 == 0:
        print(iRun)
    #抓取前40個飯店
    if iRun > 40:
        break    
    #抓取飯店名稱
    title = get_node(room,'.//h3[@data-selenium="hotel-name"]//text()',0)
    #抓取飯店星數
    star = get_node(room,'.//i[@data-selenium="hotel-star-rating"]',0)
    try:
        star = star.attrib.get('aria-label')
    except:
        star = None
    #抓取飯店地點
    location = get_node(room,'.//span[@data-selenium="area-city-text"]/text()',0)
    try:
        location = location.split('-')[0]
    except:
        location = None
    #抓取設備資訊
    adv_list = get_node(room,'.//ol[@class="Pills"]/li/text()')
    adv = ' '.join(adv_list)
    #抓取優惠卷資訊
    coupon_temp = get_node(room,'.//div[@data-element-name="coupon-promocode-badge"]/div/p/text()')
    if coupon_temp == None:
        coupon = None
    else:
        coupon = " ".join(coupon_temp)
    #抓取飯店評分
    score = get_node(room,'.//div[@class="sc-gsTCUz hjPVdY"]/p/text()',0)
    #抓取折扣前價格
    price_pre = get_node(room,'.//span[@class="sc-gKsewC fpChuk"]/text()',0)
    #抓取折扣後價格
    price_after = get_node(room,'.//span[@data-selenium="display-price"]/text()',0)
    #抓取推薦清單
    recommend = get_node(room,'.//div[@class="sc-gsTCUz kfUzYo"]/span/text()')
    if recommend != None:
        recommend = " ".join(recommend[:-1])
    #紀錄爬蟲時間
    crawler_time = time.asctime(time.localtime(time.time()))
    log_dict["title"].append(title)
    log_dict["star"].append(star)
    log_dict["location"].append(location)
    log_dict["adv"].append(adv)
    log_dict["coupon"].append(coupon)
    log_dict["score"].append(score)
    log_dict["price_pre"].append(price_pre)
    log_dict["price_after"].append(price_after)
    log_dict["recommend"].append(recommend)
    log_dict["crawler_time"].append(crawler_time)
    iRun += 1
print('finish')
df = pd.DataFrame(log_dict)
df.to_csv('agoda_result.csv',encoding = 'utf_8_sig')


