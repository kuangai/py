import time

import cx_Oracle

import fileUtil

try:
    # 建立和数据库系统的连接
    conn = cx_Oracle.connect('dbreport/dbreport@10.20.47.32:1521/ORCL')
    sql = fileUtil.readtxt()
    # 获取操作游标
    cursor = conn.cursor()
    # 执行SQL
    time1 = time.time()
    res = cursor.execute(sql)
    data = res.fetchall()
    time2 = time.time()
    times = time2 - time1
    for index in range(len(data)):
        print(str(index) + ":" + str(data[index]))
    print("共 " + str(data.rowcount) + "条数据")
    print("spent time " + str(times * 1000) + " ms")
except Exception as e:
    print(e)
finally:
    # 关闭连接，释放资源
    cursor.close()  # 关闭cursor
    conn.close()
    print('Completed!')
