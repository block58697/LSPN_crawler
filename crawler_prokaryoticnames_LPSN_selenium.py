from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import time
import pandas as pd
import re

options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome('/Users/taibif/Documents/Taibif/TaiCOL/chromedriver', chrome_options=options)
chrome.get("https://lpsn.dsmz.de")




df = pd.read_csv("/Users/taibif/Documents/Taibif/TaiCOL/file.csv")
df = df['name']
for i in df.head(4):
    print(i)

    
    search = chrome.find_element_by_name('word')
    search.send_keys(i)
    search.submit()
    
    time.sleep(1)
    
    r1 = requests.get(chrome.current_url)
    r1.encoding = "utf-8"
    web_context_re = r1.text
    #web_content_lxml_1 = etree.HTML(r1.content)
    
    #author
    author = r'Name:</b>(.*?)</p' 
    texts_author = re.findall(author, web_context_re, re.S|re.M)
    for ta in texts_author:
        ta = ta.replace('<I>','').replace('</I>','').replace('<b>','').replace('</b>','').lstrip().rstrip()
        if i in ta:
            ta = ta.replace(i, '').lstrip()
            print(ta)
        else:
            print(ta)        
            
    #references
    reref = r'publication:</b>(.*?)</p' 
    texts = re.findall(reref, web_context_re, re.S|re.M)
    for m in texts:
        m = m.replace('<i>','').replace('</i>','').replace('<b>','').replace('</b>','').lstrip().rstrip()
        if "<a href=" in m:
            reref2 = r'publication:</b>(.*?)<a'
            texts2 = re.findall(reref2, web_context_re, re.S|re.M)
            for m in texts2:
                m = m.replace('<i>','').replace('</i>','').replace('<b>','').replace('</b>','').lstrip().rstrip()
                #print(m)
        else:
            print(m)
    
    time.sleep(0.5)
    
    chrome.find_element_by_link_text("parent").click() #click parent 跳轉頁面
    print(chrome.current_url)
    
    #familyname
    r2 = requests.get(chrome.current_url)
    r2.encoding = "utf-8"
    web_context_re2 = r2.text
    
    familyname_re = r'Parent taxon:</b>(.*?)/I' 
    texts_familyname = re.findall(familyname_re, web_context_re2, re.S|re.M)
    for tf in texts_familyname:
        familyname_re2 = '<I>(.*?)<'
        texts_familyname2 = re.findall(familyname_re2, tf, re.S|re.M)
        for tf2 in texts_familyname2:
            print(tf2)
    chrome.refresh()
    
    
chrome.quit()





