import datetime
from pprint import pprint
from time import time, sleep
import sys
import requests
from bs4 import BeautifulSoup
import cralwertest2_2 as maincral
import save_db
import key_test
from cralwer2 import cral2
from cralwer3 import cral3

headers = {'USER-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
type = [100,101,102,103,104,105]
# type = [100,101]
type2 = [100]
time2 = datetime.datetime.now()
type_name = {100:'정치',101:'경제',102:'사회',103:'생활',104:'세계',105:'과학'}
def n_cralwer(time_K,type):
    sleep(2)
    # print(type_name[type])
    times = True
    doms = []
    # 10번째까지 수집
    for i in range(1,10):
        try:
            sleep(0.5)
            today = str(datetime.date.today()).replace('-','')
            url = 'https://news.naver.com/main/list.nhn?mode=LSD&sid1={}&mid=sec&listType=title&date={}&page={}'.format(type,today,str(i))
            result = requests.get(url, headers=headers)
            # print(result)
            dom = BeautifulSoup(result.text, 'lxml')
            doms.append(dom)
        except:
            continue

    # 수집된 데이터를 추가 크롤
    for dom in doms:
        try:
            div = dom.find(class_ = "list_body")
            div = div.find_all(class_ = 'type02')
            for div in div:
                try:
                    div = div.find_all('li')
                    # print("li크롤")
                    for div in div:
                        #pprint(div)
                        news_title = div.find('a').text
                        news_url = div.find('a').get('href')
                        news_times = div.find(class_ = 'date').text
                        set, news_main, news_img  = maincral.cral(news_url)

                        # DB 저장 금지일경우 건너뜀
                        if set == False:
                            break

                        print("{} {} {}\n{}\n{}\n{}".format(news_title,news_times,type,news_url,news_main,news_img))
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

                        # db에 저장
                        dateline = time2 - datetime.timedelta(minutes=int(news_times[:-1][0]))
                        print(dateline)
                        try:
                            # print("Error")
                            save_db.insert_news(news_title,news_main,news_img,type+1,news_url,dateline)
                        except:
                            print("DB 저장 오류")
                            continue
                    # 시간이 35분 이후거나 단위가 분이 아닌경우
                    if times == False:
                        #print("탈출")
                        break
                except:
                    print('페이지별 오류')
                    continue

            # 시간이 35분 이후거나 단위가 분이 아닌경우
            if times == False:
                #print("탈출")
                break
        except:
            print('전체오류')
            continue

    # 데이터 분석
    print('{} 데이터 분석 시작'.format(str(type+1)))
    key_test.key_label(time_K, str(type+1))
    print('{} 데이터 분석 시작'.format(str(type+1)))


if __name__ == '__main__':
    # 시간 설정 (30분 간격)
    time_K = datetime.datetime.now()
    minute = time_K.minute
    if minute < 30:
        time_K = time_K.replace(minute=0)
    else:
        time_K = time_K.replace(minute=30)
    time_K = str(time_K.replace(second=0))[:19]

    print('시작')
    # 멀티코어 활용
    import multiprocessing
    procs = []
    p = multiprocessing.Process(target=cral2)
    p.start()
    procs.append(p)
    p = multiprocessing.Process(target=cral3)
    p.start()
    procs.append(p)
    for type_subject in type:
        p = multiprocessing.Process(target=n_cralwer, args=(time_K, type_subject))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    sys.exit()
