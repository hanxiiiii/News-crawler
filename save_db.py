import datetime

import pymysql
# print(pymysql)
time = datetime.datetime.now()
minute = time.minute
if minute<30:
    time = time.replace(minute=0)
else:
    time = time.replace(minute=30)
time = str(time.replace(second=0))[:19]
# print(time)

# print('DBEB')
pension_db = pymysql.connect(
    user='root',
    passwd='1234',
    host='127.0.0.1',
    port=3306,
    db='newstopic',
    charset='utf8'
)
cursor = pension_db.cursor(pymysql.cursors.DictCursor)

def insert_news(title,content,img,subject,url,dateline):
    # sql = "SELECT * FROM `room`;"
    # print("EEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRR")
    sql = "INSERT INTO news(news_title,news_content,news_img,news_writetime,news_subject,news_url,news_dateline) " \
          "values(%s,%s,%s,%s,%s,%s,%s)"
    val = (title,content.strip(),img,time,subject,url,dateline)
    print(val)
    cursor.execute(sql, val)
    pension_db.commit()


