# -*- coding: utf-8 -*-
"""
@author: user
"""

from lxml import etree  
import requests
from selenium import webdriver
import pandas as pd
import csv
import time
import datetime

def crawler():  
    #開啟瀏覽器
    browser = webdriver.Chrome()
    browser.get("https://www.ettoday.net/news/focus/焦點新聞/")
    for i in range(10):
        #下拉網頁以顯示更多新聞
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        #等待網頁讀取資訊
        time.sleep(5)
    html = browser.page_source
    #產生xpath樹的root
    root = etree.HTML(html.encode('utf-8'))
    log_dict = {"report_time":[], "title":[], "article":[], "hyper_link":[]}
    #走訪儲存每個新聞的div節點
    for row in root.xpath("//div[@class='piece clearfix']"):
        try:
            article_herf = row.xpath("./a/@href")[0]
        except:
            continue
        hyper_link = "https://www.ettoday.net/news{}".format(article_herf)
        #打開新聞分頁
        article_result = requests.get(hyper_link)
        article_root = etree.fromstring(article_result.text, etree.HTMLParser())
        try:
            #抓取新聞報導時間
            report_time = article_root.xpath("//div[@class='c1']/div/div/time/@datetime")[0]
            #抓取新聞標題
            title = (article_root.xpath("//div[@class='c1']/div/article/div/header/h1/text()")[0]).lstrip().rstrip()#儲存標題 
        except:
            continue
        #抓取新聞每個段落，新聞的段落被儲存在特定的p標籤裡
        article = ""
        for paragraph in article_root.xpath("//div[@class='c1']/div/article/div/div[@class='story']/p"):
            temp = paragraph.xpath("./text()")
            if len(temp) > 0:
                article += temp[0]
        log_dict["report_time"].append(report_time)
        log_dict["title"].append(title)
        log_dict["article"].append(article)
        log_dict["hyper_link"].append(hyper_link)
    return log_dict

log_dict = crawler()
df = pd.DataFrame(log_dict)
df.to_csv("et_result.csv", encoding = "utf_8_sig", index = None)
    