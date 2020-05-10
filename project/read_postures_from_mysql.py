# -*- coding: utf-8 -*-
  
import pandas as pd
import pymysql
  
## 加上字符集参数，防止中文乱码
dbconn=pymysql.connect(
  host="127.0.0.1",
  database="birth",
  user="taimeng",
  password="meng",
  port=3306,
  charset='utf8'
 )
  
#sql语句
sqlcmd="select num,frequency,expectant from pre_alert"
  
#利用pandas 模块导入mysql数据
a=pd.read_sql(sqlcmd,dbconn)
#取前5行数据
#b=a.head()
print(a)
  
