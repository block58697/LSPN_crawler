import requests
import csv
import pandas as pd
import re


df = pd.read_csv("/Users/taibif/Documents/Taibif/TaiCOL/file_taxonomic_status.csv") #讀檔
df = df['name']

with open ("/Users/taibif/Documents/Taibif/TaiCOL/file_test2.csv",'w') as csvfile: #寫入

    rows = csv.DictReader(csvfile)
    fieldnames = ['name', 'author', 'reference', 'family', 'status']
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()
    
    for i in df:
    
        print(i)
        i_sp = i.replace(' ','-').lower()
        #print(i_sp)
        url_sp = 'https://lpsn.dsmz.de/species/'+i_sp
        #print(url_sp)
           
        
        i_genus = i.split(' ')
        i_genus = i_genus[0].lower()
        url_genus = 'https://lpsn.dsmz.de/genus/'+i_genus
        
        #print(url_genus)
    
        #time.sleep(1)
        
        r1 = requests.get(url_sp)
        r1.encoding = "utf-8"
        web_context_re = r1.text
        #web_content_lxml_1 = etree.HTML(r1.content)
        
        #author
        author = r'Name:</b>(.*?)</p' # 擷取命名者
        texts_author = re.findall(author, web_context_re, re.S|re.M)
        for ta in texts_author:
            ta = ta.replace('<I>','').replace('</I>','').replace('<b>','').replace('</b>','').lstrip().rstrip()
            if i in ta:
                ta = ta.replace(i, '').lstrip()
                print(ta)
            else:
                print(ta)    
                
        #references
        reref = r'publication:</b>(.*?)</p'  # 擷取文獻
        texts = re.findall(reref, web_context_re, re.S|re.M)
        for m in texts:
            m = m.replace('<i>','').replace('</i>','').replace('<b>','').replace('</b>','').lstrip().rstrip()
            if "<a href=" in m:
                reref2 = r'publication:</b>(.*?)<a'
                texts2 = re.findall(reref2, web_context_re, re.S|re.M)
                for m in texts2:
                    m = m.replace('<i>','').replace('</i>','').replace('<b>','').replace('</b>','').lstrip().rstrip()
                    print(m)
            else:
                print(m)
 
        #Taxonomic status # 擷取命名狀態
        status = r'Taxonomic status:</b>(.*?)</p' 
        texts_status = re.findall(status, web_context_re, re.S|re.M)
        for ts in texts_status:
            ts = ts.lstrip().rstrip()
            print(ts)
        
        #familyname
        r2 = requests.get(url_genus)
        r2.encoding = "utf-8"
        web_context_re2 = r2.text
        
        familyname_re = r'Parent taxon:</b>(.*?)/I' 
        texts_familyname = re.findall(familyname_re, web_context_re2, re.S|re.M)
        for tf in texts_familyname:
            familyname_re2 = '<I>(.*?)<'
            texts_familyname2 = re.findall(familyname_re2, tf, re.S|re.M)
            for tf2 in texts_familyname2:
                print(tf2)
        list_R = [ta, m, ts, tf2]
        #print(list_R)
    
        writer.writerow({'name':i, 'author':ta, 'reference':m, 'family':tf2, 'status':ts})
    
    
    
    
