# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 16:46:21 2023

@author:
"""

from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By

browser=webdriver.Chrome()
browser.get('https://www.beijing.gov.cn/so/s?siteCode=1100000088&tab=zcfg&qt=%E4%BA%BA%E6%89%8D%E5%BC%95%E8%BF%9B')
time.sleep(5)

lable=browser.find_elements(By.CSS_SELECTOR,'.position-con.item-choose')#查找全文和标题的检索项
print(lable[0].text,lable[1].text)
js= 'arguments[0].setAttribute(arguments[1],arguments[2])'
browser.execute_script(js,lable[0],'class','position-con item-choose')#修改全文标签的class
browser.execute_script(js,lable[1],'class','position-con item-choose item-choose-on')#修改标题标签的class


time.sleep(2)
data=pd.DataFrame([],columns=['类型','链接','标题','文号','发文机构','主题分类','发布日期'])
page=1
while page:
    if page !=1:
        page.click()
        time.sleep(1)
    poli=browser.find_elements_by_class_name('search-result')
    for elements in poli:#一个elements是一个记录
        p_type=elements.find_element_by_class_name("result-header-lable").text#政策类型
        link=elements.find_element_by_tag_name("a").get_attribute('href')#链接
        title=elements.find_element_by_tag_name("a").text#标题
        table=elements.find_elements_by_class_name("row-content")#文号、发文机构、主题分类、发布日期
        content=[p_type,link,title]
        for item in table:
            content.append(item.text)
        while len(content)<7:
            content.append(0)
        content=pd.DataFrame([content],columns=['类型','链接','标题','文号','发文机构','主题分类','发布日期'])
        data=pd.concat([data,content])
    page=browser.find_element_by_class_name('next')
data.to_csv(r'人才政策爬取\北京市人才政策.csv',encoding='utf_8_sig',index=False)
