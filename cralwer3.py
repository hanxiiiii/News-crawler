import datetime
import os
import sys
from pprint import pprint
import time

import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import save_db
import key_test

# 시간 설정 (30분 간격)
time_K = datetime.datetime.now()
minute = time_K.minute
if minute < 30:
    time_K = time_K.replace(minute=0)
else:
    time_K = time_K.replace(minute=30)
time_K = str(time_K.replace(second=0))[:19]

sys.path.append("C:/cla/")
import stopword2
stopword = stopword2.stopword
def cral3():
    print("크롤러3(스포츠) 시작")
    time2 = datetime.datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    headers = {'USER-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
               , 'Pragma':'no-cache'}
    times = True
    url = 'https://sports.daum.net/news/breaking'
    while(True):
        try:
            #driver = webdriver.Chrome(executable_path='chromedriver') # , chrome_options=chrome_options)
            driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
            print("드라이버동작")
            driver.get(url=url)
            for i in range(1,10):
            # 오류 방지 0.5초 대기
                time.sleep(1)
                driver.find_element_by_class_name('link_moreview').click()

            html = driver.page_source
            dom = BeautifulSoup(html, 'html.parser')
            print("페이지 문제")
            # pprint(dom)
            div = dom.find(class_ = "list_news")
            div = div.find_all('li')
            print("li 문제")
            break
        except:
            time.sleep(30)
            continue

    for div in div:
        try:
            img = div.find('img')
            if img != None:
                img = 'https://'+img.get('src')[2:]
                # print(img)

            content = div.find(class_ = 'wrap_cont')
            news_title = content.find(class_ = 'link_txt').text
            news_url = content.find(class_ = 'link_txt').get('href')
            news_content = content.find(class_ = 'link_desc').text

            for i in stopword:
                news_content = news_content.replace(i," ")

            news_time = content.find(class_ = 'txt_num').text[4:]
            # print(news_time)

            # DB 저장 금지 일경우
            if news_content.find('DB') != -1:
                continue

            # 방금 전은 1분전으로 처리
            if(news_time == '방금 전'):
                news_time = '1분 전'

            news_times = news_time.split("분")
            # print(news_times[0])
            # 시간이 35분 이후거나 단위가 분이 아닌경우
            if int(news_times[0]) > 35:
                times = False
                break
            elif news_times[1] == None:
                times = False
                break

            dateline = time2 - datetime.timedelta(minutes=int(news_times[:-1][0]))
            print("{} {} {} \n{} \n{}\n{}".format(news_title,news_time,dateline,news_url,news_content,img))
            # print(news_content)
            print("----------------"*4)
            save_db.insert_news(news_title, news_content, img, 108, news_url,dateline)

        except:
            print('전체오류')
            continue




    print("크롤링 종료")
    driver.quit()
    # 데이터 분석
    print('데이터 분석 시작')
    key_test.key_label(time_K, '108')
    print('데이터 분석 종료')
