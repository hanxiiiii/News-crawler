import sys

import pymysql
sys.path.append("C:/cla/")
import stopword2
stopword = stopword2.stopword

pension_db = pymysql.connect(
    user='root',
    passwd='1234',
    host='127.168.0.1',
    port=3306,
    db='newstopic',
    charset='utf8'
)
cursor = pension_db.cursor(pymysql.cursors.DictCursor)

break_one = []

stopwd =[]

# db 저장
def key_save(key,sub_count,subject,ti,news_list) :
    sql = "insert into keyword(keyword, keyword_set_number,subject_id,keyword_writetime,keyword_news_list) " +\
          "values(%s,%s,%s,%s,%s)"
    val = (key, sub_count, subject, ti, news_list)
    cursor.execute(sql, val)
    pension_db.commit()

# 있는지 판단
def key_look(ti,subject):
    sql = "select count(*) from keyword where keyword_writetime='{}' and subject_id='{}'".format(ti,subject)
    # sql = "select count(*) from news where news_subject=109;"
    cursor.execute(sql)
    res = cursor.fetchall()[0]['count(*)']
    return res

# 기사글 찾기
def key_like(cursor,time,subject,keyword):
    sql = 'select * FROM news where news_writetime ="{}" and news_subject = "{}" ' \
          'and (news_title like "%{}%" or news_content like "%{}%");'.format(time,subject,keyword,keyword)
    # print(sql)
    cursor.execute(sql)
    res = cursor.fetchall()
    keys = ""
    # print("test")
    # print(keyword,res)
    for data in res:
        keys = keys + str(data['news_id']) + ','
        # print(data['news_id'],data['news_title'],data['news_writetime'],data['news_content'])
    keys = keys[:-1]
    return keys


# 키워드분석
def key_label(ti,subject):
    try:

        print("분석 여부 판단")
        if key_look(ti,subject) != 0:
            print("이미 분석된 시간과 키워드입니다.")
            return 0;

        print("스탑워드 불러오기")
        # 스탑워드 불러오기
        if subject == '101':
            stopwd = stopword2.stopword_101
        elif subject =='102':
            stopwd = stopword2.stopword_102
        elif subject =='103':
            stopwd = stopword2.stopword_103
        elif subject =='104':
            stopwd = stopword2.stopword_104
        elif subject =='105':
            stopwd = stopword2.stopword_105
        elif subject =='106':
            stopwd = stopword2.stopword_106
        elif subject =='107':
            stopwd = stopword2.stopword_107
        elif subject =='108':
            stopwd = stopword2.stopword_108
        else:
            print('subject값이 잘못되었습니다')
            return 0;

        print("데이터 불러오기")
        # 데이터 불러오기
        sql = 'select * FROM news where news_writetime = "{}" and news_subject = {};'.format(ti,subject)
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(stopword)
        news_data = ""
        # print(len(res))

        print("내용 통합")
        # 내용 통합
        for data in res:
            news_data = news_data + data['news_title'] +data['news_content']


        print("1차 키워드 제외")
        # 1차 키워드 제외
        for i in stopword:
            news_data = news_data.replace(i, "")
        # print(news_data)


        # 횟수 분석
        def listset(malist):
            print('횟수 분석')
            count={}
            for i in malist:
                try: count[i] += 1
                except: count[i]=1
            # print(count)

            if count == []:
                print('데이터가 없습니다')
                return 0;


            # 2차 키워드 제외
            print('2차 키워드 제외')
            for i in stopwd:
                try:
                    del count[i]
                except:
                    continue



            # 내림차순 정렬
            print('내림차순 정렬')
            count2 = sorted(count.items(),reverse=True,  key= lambda item : item[1])
            try:
                for ccc in count2:
                    if len(ccc[0]) ==1:
                       try:
                           if break_one.index(ccc[0]) >= 0:
                               pass
                       except:
                          break_one.append(ccc[0])
            except:
                pass

            # 상위 20개만 분리
            count2 = count2[:20]
            # print(count2)

            # 20개에 해당하는 뉴스기사 목록
            for key in count2:
                # print(key[0]+"\n", key_like(cursor,ti,subject,key[0]))
                key_likes = key_like(cursor,ti,subject,key[0])

                # db 저장
                try:
                    print('{} {} {} {} {}'.format(key[0], key[1], subject, ti, key_likes))
                    key_save(key[0], key[1], subject, ti, key_likes)
                except:
                    print("{} {} DB저장 오류".format(ti,subject))
                    continue

            return count2


        # 형태소 분리 및 키워드 제외
        print("분석 시작")
        from konlpy.tag import Okt
        print('******************\n'*40)
        okt=Okt()
        malist = okt.nouns(news_data)
        print('----------------\n' * 40)
        print(ti+" ",subject+"\n",listset(malist))
    except:
        print('전체오류')
        return 0


# print('시작')
# subject = ['101','102','103','104','105','106','107','108']
# for subject in subject:
#     for i in range(17,28):
#         for t in range(0,24):
#             key_label('2021-06-{} {}:00:00'.format(i, t), subject)
#             key_label('2021-06-{} {}:30:00'.format(i, t), subject)
# print('종료')