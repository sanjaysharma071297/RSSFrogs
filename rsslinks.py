# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 10:58:48 2020

@author: Sanjay Sharma
"""

import time
import pyodbc
from selenium import webdriver
from bs4 import BeautifulSoup 
from urllib.request import urlopen
import pandas as pd
import os

def database_connect():
    """
    conncet Sfrogs Databse
    """
    server = os.getenv('DEV_SERVER')
    database = 'sfrogs'
    username = os.getenv('DEV_SERVER_USERNAME')
    password = os.getenv('DEV_SERVER_PASSWORD')
    driver = '{ODBC Driver 17 for SQL Server}'

    con = None
    i = 0
    while i < 5:
        try:
            con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        except:
            i += 1
            print('facing issues while connecting to the DB, trying again in 30 seconds...')
            time.sleep(30)
            continue
        finally:
            if con != None:
                break
    return con



url='https://www.businesswire.com/portal/site/home/news/industries/'

browser=webdriver.Chrome()
browser.maximize_window()

count=1
title,rss_link=[],[]
   
browser.get(url) # open url in browser
browser.set_page_load_timeout(100) 
page_source = browser.page_source 
soup = BeautifulSoup(page_source,'lxml') 

con = database_connect()
cur = con.cursor()

table=soup.findAll("td" , {"class" : "dataConstant rss"})
for tag in table:
    rsstitle = tag.get("title")
    #print(rsstitle)
    title.append(rsstitle)
    #id.append(count);count+=1

    
link=soup.findAll("a" , {"class" : "icon"})
for l in link:
    url = l.get("href")
    #print(url)
    rss_link.append(url)

for tit,lin in zip(title,rss_link):
    try:
        cur.execute('insert into RSSLinks(rsstitle,rsslinks) values(?,?)',(tit,lin))
        cur.commit()
    except:pass
    
con.close()

#data=pd.DataFrame({"Id": id ,"RSS_Title": title , "RSS_Link":rss_link})

#data.to_excel("RssLink.xlsx", index=False)



     
    


