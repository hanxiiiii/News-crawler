from pprint import pprint
from time import time, sleep

import requests
from bs4 import BeautifulSoup
import sys
sys.path.append("C:/cla/")
import stopword2

stopword = stopword2.stopword
def cral(url):
    set = True
    headers = {'USER-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
    sleep(0.5)
    result = requests.get(url, headers=headers)
    # print(result)
    dom = BeautifulSoup(result.text, 'lxml')
    div = dom.find(class_ = "article_body")
    div = div.find(class_ = '_article_body_contents')
    # pprint(div)
    # print("---------------------------------------")
    # 광고 분류
    stop = div.find_all('a')
    for i in div.find_all('script'):
        # print(i)
        stop.append(i)
    # for i in stop:
    #     print(i.text)

    # DB 저장 금지 여부 판단
    if div.text.find('DB') != -1:
        set = False
        return set,0,0;
    else:
        mains = div.text.strip()
        for i in stop:
            # print(i.text)
            mains = mains.replace(i.text.strip(), " ")
            # print(mains)
        # print("************************************")
        # print(div.text)
        # print("************************************")
        mains = mains.replace("\n","").replace("\t","")
        # print(mains)
        #링크가 들어가 있는 광고 삭제


        for i in stopword:
            mains = mains.replace(i, "")


        mains = mains.rstrip()

        # print(mains)
        img = div.find('img')
        if img != None:
            img = img.get('src')
        # print(mains)
        return set, mains, img


# url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=092&aid=0002224886'
# url2 = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=105&oid=021&aid=0002474720'
# url = 'https://entertain.naver.com/now/read?oid=421&aid=0005417708'
# url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=sec&sid1=101&oid=421&aid=0005445338'
# set, mains, img = cral(url)
# print(set)
# print(mains)
# print(img)