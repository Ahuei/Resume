import requests
import re
import time
import threading
import pymysql


def write2database(list_content, table_name, event_time):
    db = pymysql.connect(host="localhost",
                        user="root",
                        password="123456",
                        port=3306,  # 端口
                        database="wbhot",
                        charset='utf8')
    cursor = db.cursor()
    # sql = "CREATE DATABASE IF NOT EXISTS wbhot" 
    # # 执行创建数据库的sql
    sql = "create table if not exists {}(time char(5), event_name char(30), heat int)".format(table_name)
    cursor.execute(sql)
    db.commit()

    sql_content = "INSERT INTO {} values(%s, %s, %s)".format(table_name)
    try:
        for i in range(len(list_content)):
            cursor.execute(sql_content, (event_time, list_content[i][0], int(list_content[i][1])))
        print('Write data to DB---Success')
        db.commit()
    except:
        print("Write data to DB---Fail")

    db.close()

def wbhot():
    global timer
    url = "https://s.weibo.com/top/summary?cate=realtimehot"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363"
    }

    try:
        response = requests.get(url, headers=headers)
        # print("response:", response)
    except Exception as error:
        error_time = time.strftime("%Y-%m-%d-%H_%M", time.localtime())
        print("Error happened in ", error_time)
        time.sleep(60)
        wbhot()
    else:
        string = response.text
        # print(string)
        results = re.findall('<td class="td-02">.*?top.*?target="_blank">(.*?)</a>.*?<span>(.*?)</span>', string, re.S)  # list
        table_name, event_time = time.strftime("%Y_%m_%d", time.localtime()), time.strftime("%H_%M", time.localtime())
        write2database(results, table_name, event_time)

        timer = threading.Timer(300, wbhot)
        timer.start()




if __name__ == "__main__":
    wbhot()

