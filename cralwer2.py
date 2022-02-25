import datetime
import os
import sys
from pprint import pprint
import time

import requests
from bs4 import BeautifulSoup
import cralwertest2_3 as maincral
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import save_db
import key_test
def cral2():
    # 시간 설정 (30분 간격)
    time_K = datetime.datetime.now()
    minute = time_K.minute
    if minute < 30:
        time_K = time_K.replace(minute=0)
    else:
        time_K = time_K.replace(minute=30)
    time_K = str(time_K.replace(second=0))[:19]


    # 셀리니움 시작
    print("크롤러2(연예) 시작")
    time2 = datetime.datetime.now()
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    headers = {'USER-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
               , 'Pragma':'no-cache'}
    times = True
    doms=[]
    for i in range(1,21):
        try:
            today = str(datetime.date.today())
            url = 'https://entertain.naver.com/now#sid=106&date={}&page={}'.format(today,str(i))
            print(url)
            driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=chrome_options)
            print("드라이버동작")
            driver.get(url=url)
            print("페이지 문제")
            # 오류 방지 0.5초 대기
            time.sleep(0.5)
            html = driver.page_source
            dom = BeautifulSoup(html, 'html.parser')
            # print(dom)
            doms.append(dom)
            print("dom 문제")
        except:
            print('스크랩 오류')
            continue

    # for i in doms:
    #     print(i)
    #     print('-'*40)

    for dom in doms:
        try:
            div = dom.find(class_ = "news_lst")
            div = div.find_all('li')
            for div in div:
                try:
                    # pprint(div)
                    div = div.find(class_ = "tit_area")
                    # pprint(div)
                    news_title = div.find('a').text
                    news_url = "https://entertain.naver.com" + div.find('a').get('href')
                    news_times = div.find('em').text
                    print("{} {}\n{}".format(news_title,news_times,news_url))
                    # print("-"*40)
                    set, news_main, news_img  = maincral.cral(news_url)
                    # DB 저장 금지일경우 건너뜀
                    if set == False:
                        break

                    # db저장부분으로 변경
                    # print("{}\n{}".format(news_main,news_img))
                    print("{} {}\n{}\n{}\n{}".format(news_title,news_times,news_url,news_main,news_img))
                    print("--------------"*4)

                    news_times = news_times.split("분")
                    # print(news_times[0])
                    # 시간이 35분 이후거나 단위가 분이 아닌경우
                    if int(news_times[0]) > 35:
                        times = False
                        break
                    elif news_times[1] == None:
                        times = False
                        break
                    dateline = time2 - datetime.timedelta(minutes=int(news_times[:-1][0]))
                    print(dateline)
                    save_db.insert_news(news_title, news_main, news_img, 107, news_url,dateline)

                except:
                    print('개별 오류')
                    continue
            # 시간이 35분 이후거나 단위가 분이 아닌경우
            if times == False:
                #print("탈출")
                break
        except:
            print('전체 오류')
            continue

    print("크롤링 종료")
    driver.quit()
    # 데이터 분석
    print('데이터 분석 시작')
    key_test.key_label(time_K, '107')
    print('데이터 분석 종료')
