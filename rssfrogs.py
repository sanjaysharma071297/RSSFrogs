
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 13:58:33 2020
Working: Program will take input from RssLinks and Extract the data from the given links
@author: Sanjay Sharma
"""

import pyodbc
#from selenium import webdriver
from bs4 import BeautifulSoup
import urllib.request
import requests
import pandas as pd
import os
import time

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

def select_data_from_database(con,query):
    """
    function take SQL query and SQL connection  as input  and give the result of query as DataFrame
    Args:
    -------
        con :- SQL Connectivity from the DataBase
        query :- SQL select Query like 'select  * from table'
    Returns:
    -----------
        return table as DataFrame of sql query's result
    """
    table = pd.read_sql_query(query,con)
    return table

con = database_connect()
cur = con.cursor()

#Selecting the rss links from where we need to extract data
table  = select_data_from_database(con,"select id,rsslinks from RSSlinks where id in \
(11,12,16,18,52,53,79,89,95,100,108,117,118,119,120,121,122,124,155,156,191,193,194,195,196,197,198,199,200,204,205,206,222)")

title,description,link,date,rsslinkid=[],[],[],[],[]
count=0
for index,row in table.iterrows():
    print(index,end = "\t")
    urll = 'http:' + row["rsslinks"]
    print(urll)
    try:
        page = requests.get(urll)
        soup = BeautifulSoup(page.text,'xml')              
        xml=soup.findAll('item') 
        
        #Finding title,link,description,publish date from the xml and in xml item tag
        for tag in xml:
            rss_title= tag.find('title').text
            title.append(rss_title)
            
            rss_link=tag.find('link').text
            link.append(rss_link)
            
            rss_description=tag.find('description').text
            description.append(rss_description)
            
            rss_pubdate=tag.find('pubDate').text
            d = ' '.join(rss_pubdate.split()[1:4])
            date.append(d)
            
            rsslinkid.append(row["id"])
    except:pass
    
for tit,des,lin,dat,rssid in zip(title,description,link,date,rsslinkid):
    try:
        cur.execute('insert into RSSDataTemp(ItemTitle,ItemDescription,ItemLink,PublishDate,RssLinkId) values(?,?,?,?,?)',(tit,des,lin,dat,rssid))
        cur.commit()
    except:pass
    
con.close()

'''
data=pd.DataFrame({"RSS_Title": title , "RSS_Description": description,"RSS_Link":link, "PublishDate": date, "rsslinkid":Id})
        
data.to_excel("Rssdatatest8.xlsx", index=False)'''




