import subprocess
from datetime import datetime
import redis
import pymysql
import time


redis_ret = ""
mysql_ret = ""

start_time = datetime.now()


while True:
    try:
        redis_server = redis.StrictRedis(host="localhost", password="tesunet")
        redis_ret = redis_server.ping()
    except:
        pass

    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='password',
                                     db='mysql',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection.cursor() as cursor:
            sql = "SELECT user, host FROM user;"
            cursor.execute(sql)
            mysql_ret = cursor.fetchall()
    except:
        pass

    if redis_ret and mysql_ret:
        try:
            subprocess.run(
                r'cmd /k "cd /d D:\Pros\TSDRM&&python manage.py celery -A TSDRM flower -l info')
        except:
            print("celery goes error...")
        break
    else:
        print("mysql or redis server is not running...")

    end_time = datetime.now()
    try:
        delta_time = end_time-start_time

        # 15分钟后没有启动redis/mysql则停止循环
        if delta_time.total_seconds() >= 60*15:
            break
    except:
        pass

    time.sleep(5)




