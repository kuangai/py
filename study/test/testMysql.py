#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb,json

# 打开数据库连接
con = MySQLdb.connect("localhost", "root", "123456")
# db = MySQLdb.connect("localhost", "testuser", "test123", "TESTDB", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = con.cursor()

# 创建数据库
try:
    cursor.execute('create database testpy default character set utf8mb4 collate utf8mb4_general_ci;')
    print("--------------Create database testpy success！--------------")
except:
    print("--------------Database testpy exists!--------------")


con.select_db('testpy')

# 如果数据表已经存在使用 execute() 方法删除表。
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 创建数据表SQL语句
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)
print("--------------CREATE TABLE EMPLOYEE SUCCESS！--------------")


insertSql = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""

insertSqlWithParamsMap = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac1', 'Mohan1', 201, %(sex)s, %(icome)s)"""

insertSqlWithParamsArr = """INSERT INTO EMPLOYEE(FIRST_NAME,
         LAST_NAME, AGE, SEX, INCOME)
         VALUES ('Mac2', 'Mohan2', 20, %s, %s)"""
try:
   cursor.execute(insertSql)

   sex = "F"
   icome = 1000
   # 数组传参
   cursor.execute(insertSqlWithParamsArr,[sex,icome])

   # 字典传参
   map = {"sex":sex,"icome":icome}
   cursor.execute(insertSqlWithParamsMap,map)
   con.commit()
   print("--------------插入数据成功并提交事务！--------------")
except:
   con.rollback()
   print("--------------插入数据出现异常，已回滚！--------------")

sql = "select * from employee"
cursor.execute(sql)

# 取出下一条记录
result = cursor.fetchone()
print("--------------取出下一条记录: " + str(result) + "--------------")
# 取出剩余所有记录
result = cursor.fetchall()
print("--------------取出剩余所有记录: %s --------------" % str(result))
# sql 执行后的受影响的行数
print("--------------受影响的行数: %s --------------" % cursor.rowcount)

# mysql2json
column_list = []
fields = cursor.description
for field in fields:
    column_list.append(field[0])
date_list = []
for row in result:
    date = {}
    for k in range(0, len(fields)):
        date[column_list[k]] = str(row[k])
    date_list.append(date)

print("结果集转为json：%s" % json.dumps(date_list))

# 关闭数据库连接
con.close()