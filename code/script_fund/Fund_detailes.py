import requests
import pymysql

# url = "https://api.doctorxiong.club/v1/fund?code="
# fund_num = "161725"
# url = url + fund_num
# url = "https://api.doctorxiong.club/v1/fund/all"
# print(url)
# content = requests.get(url).json()
# print(content)
# print(type(content))
# print(content["data"])
# print(type(content["data"][0]["name"]))
# print(content["data"][0]["name"])

def GetBasicInformation(fund_num):
    url_root = "https://api.doctorxiong.club/v1/fund?code="
    # fund_num = str(fund_num)
    url = url_root + str(fund_num)
    # url = "https://api.doctorxiong.club/v1/fund/all"
    # print(url)
    content = requests.get(url).json()
    # print(content)
    # print(type(content))
    print(content["data"])
    
    return content["data"]

def GetAllFunds():
    url = "https://api.doctorxiong.club/v1/fund/all"
    fund_ID = []  # 基金代码
    try:
        content = requests.get(url).json()
    except Exception as err:
        pass
    else:
        for num in content["data"]:
            fund_ID.append(num[0])  # 获得所有基金代码
    print(fund_ID)

    WriteFundNum2Database(fund_ID)

def WriteFundNum2Database(fund_ID):
    db = pymysql.connect(host="localhost",
                        user="root",
                        password="123456",
                        port=3306,  # 端口
                        database="fund",
                        charset='utf8')
    cursor = db.cursor()
    # sql = "CREATE DATABASE IF NOT EXISTS wbhot" 
    # # 执行创建数据库的sql
    sql = "create table if not exists fund_id_all(id int, Fund_ID char(5))"
    cursor.execute(sql)
    db.commit()

    sql_content = "INSERT INTO fund_id_all values(%s, %s)"
    try:
        for i in range(len(fund_ID)):
            cursor.execute(sql_content, (i, fund_ID[i]))
            print("fund_ID[i]:", fund_ID[i])
        print('Write data to DB---Success')
        db.commit()
    except:
        print("Write data to DB---Fail")

    db.close()



if __name__ == "__main__":
    # fund_num = 161725
    # GetBasicInformation(fund_num)
    GetAllFunds()