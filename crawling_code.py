import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager # setting up the chromedriver automatically using webdriver_manager

import json
import sys
from tqdm import tqdm
import pandas as pd
import os

import mysql.connector
from mysql.connector.constants import ClientFlag

import requests
from bs4 import BeautifulSoup


def crawler_url(page_num):
    
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=1920,1080')
    final=[]
    df=pd.DataFrame(columns=['title', 'summary', 'who', 'criteria', 'what', 'how', 'call', 'site'])
    driver_path=os.getcwd()+'\crawler\chromedriver.exe'
    driver = webdriver.Chrome(driver_path, options=options) #ChromeDriverManager().install()
    page_num=int(page_num)

    for page in tqdm(range(1,page_num+1),mininterval=1):
        url= "https://www.bokjiro.go.kr/welInfo/retrieveWelInfoBoxList.do?searchIntClId=06&searchCtgId=&welInfSno=&searchWelInfNm=&pageGb=&domainName=&searchSidoCode=&searchCggCode=&cardListTypeCd=list&welSrvTypeCd=01&pageUnit=10&pageIndex="+str(page) 
        
        try:
            driver.get(url)
            driver.implicitly_wait(3)

            # page 당 10개씩 있는 정책 가져오기
            for block in tqdm(range(1,11),mininterval=1):
                
                # category를 찾아서 들어가기
                path='//*[@id="contents"]/div[4]/ul/li['+str(block)+']/div/a[2]'
                category = driver.find_element_by_xpath(path)
                category.click()
                driver.implicitly_wait(3)
                
                # category url 가져오기
                #url_list=driver.current_url
                soup = BeautifulSoup(driver.page_source, "html.parser")
                
                # title 가져오기
                title=soup.select_one('#contents > div.bokjiDetailWrap > h4 > span')
                title=title.get_text()
                
                # summary
                summary=soup.select_one('#contents > div.bokjiDetailWrap > div')
                summary=summary.get_text()
                
                # who
                if soup.select('#backup > div:nth-child(1) > div > ul > li.first > p'):   
                    path='#backup > div:nth-child(1) > div > ul > li.first > p'
                    who=soup.select_one(path)
                    who=who.get_text()
                elif soup.select('#backup > div:nth-child(1) > div > ul > li.first > ul > li'):
                    path='#backup > div:nth-child(1) > div > ul > li.first > ul > li'
                    who=soup.select_one(path)
                    who=who.get_text()
                elif soup.select('#backup > div:nth-child(1) > div > ul > li > ul > li'):
                    path='#backup > div:nth-child(1) > div > ul > li > ul > li'
                    who=soup.select_one(path)
                    who=who.get_text()
                else:
                    who=''
        
                # criteria
                if soup.select('#backup > div:nth-child(1) > div > ul > li:nth-child(2) > p'):   
                    path='#backup > div:nth-child(1) > div > ul > li:nth-child(2) > p'
                    criteria=soup.select_one(path)
                    criteria=criteria.get_text()
                elif soup.select('#backup > div:nth-child(1) > div > ul > li:nth-child(2) > ul'):
                    path='#backup > div:nth-child(1) > div > ul > li:nth-child(2) > ul'
                    criteria=soup.select_one(path)
                    criteria=criteria.get_text()
                else:
                    criteria=''
                
                
                # what
                try:
                    what=soup.select_one('#backup > div:nth-child(2) > div > ul > li > ul > li')
                    what=what.get_text()
                except:
                    what=''
                driver.implicitly_wait(3)
                
                # how
                if soup.select('#backup > div:nth-child(3) > div > ul.bokjiContsIn > li.first > ul > li'):   
                    path='#backup > div:nth-child(3) > div > ul.bokjiContsIn > li.first > ul > li'
                    how=soup.select_one(path)
                    how=how.get_text()
                elif soup.select('#backup > div:nth-child(3) > div > ul > li > ul > li'):
                    path='#backup > div:nth-child(3) > div > ul > li > ul > li'
                    how=soup.select_one(path)
                    how=how.get_text()
                else:
                    how=''
                
                # call
                try:
                    call=soup.select_one('#contents > div:nth-child(7) > div.bokjiServiceView > div > div > ul > li.phone > ul > li')
                    call=call.get_text()
                except:
                    call=''
                
                # site
                try:
                    site=soup.select_one('#contents > div:nth-child(7) > div.bokjiServiceView > div > div > ul > li.internet > ul > li')
                    site=site.get_text()
                except:
                    site=''
                
                # dataframe에 가져온 category url 저장
                idx=(page-1)*10+(block-1)
                df.loc[idx]=[title, summary, who, criteria, what, how, call, site]

                driver.back()
                driver.implicitly_wait(3)

        except:
            print('html page does not exist :', url)
            continue
    
    driver.quit()

    return df

# category url을 selenium으로 가져와서 csv 파일로 저장
os.chdir("./crawler")
config = {
    'user': 'root',
    'password': '1357',
    'host': '34.64.116.88',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'server-ca.pem',
    'ssl_cert': 'client-cert.pem',
    'ssl_key': 'client-key.pem',
    'database' : 'welfare-for-everyone'
}


result_final=df[['title', 'summary']]
result_final['welfare_id']=['100']
result_final=result_final[['welfare_id', 'title', 'summary']]

# now we establish our connection
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor(prepared=True)
query = ("""INSERT INTO welfare (welfare_id, title, summary) VALUES (%s, %s, %s)""") #table name 바꾸는 거 기억하기
input_data=[tuple(x) for x in result_final.to_records(index=False)]
cursor.executemany(query, input_data) #error 나는 이유가 tuple이 아니라 numpy.record이기 때문

cnxn.commit()  # and commit changes
cnxn.close() 

