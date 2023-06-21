# -*-coding:utf-8 -*-
# !/usr/bin/python3
import pymysql


def db_mysql():
    return pymysql.connect(host="gz-cdb-drwjswdl.sql.tencentcdb.com", port=61428, user="new_duba",
                           password="guw1wlftal0yn88ehxagdyosu2pumb", database="new_duba")


def query_paysetting(id):
    try:
        # 打开数据库连接
        db = db_mysql()
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        # 使用 execute()  方法执行 SQL 查询
        cursor.execute("SELECT * FROM pay_settings where Id=%s" % (str(id)))
        data = cursor.fetchone()
        result = {'Id': int(data[0]), 'current_price': str(data[1]),
                  'day_length': str(data[11]), 'remark': str(data[21])}
        # 关闭数据库连接
        db.close()
    except:
        print('db_failed')
        return 'db_failed'
    return result


'''
def insertUser(groupid, username, password):
    try:
        db = db_mysql()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user(groupid, username, password) VALUES (%d,'%s','%s')" % (groupid, username, password))
        db.commit()
        db.close()
    except:
        db.rollback()
        db.close()
        print('db_failed')
        return False
    return True


def changePassword(userid, newpwd):
    try:
        db = db_mysql()
        cursor = db.cursor()
        msql = ("update user set password = '%s' where userid = %d" % (newpwd, userid))
        cursor.execute(msql)
        db.commit()
        db.close()
    except Exception as e:
        db.rollback()
        db.close()
        print('db_failed')
        return False
    return True
'''

if __name__ == "__main__":
    print(query_paysetting(30))
