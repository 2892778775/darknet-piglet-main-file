import pymysql
import json
import pandas as pd

def import_data(fn):
    # 读txt文件
    f = open(fn, 'r')
    m = f.readlines()
    print(len(m))
    con = pymysql.connect(host='127.0.0.1', port=3306, user='taimeng', password='meng', db='birth', charset='utf8')
    cur = con.cursor()

    for line in m:
        A = line.strip('\n').split(',')
        A2 = []
        for a in A:
            b = a.strip(' ')
            A2.append(b)
        s = {'sowid': A2[0],'piglets':int(A2[1]),'detect_time':A[2]}  # 转成字典
        print("s[sowid]",s['sowid'])
        sqlcmd="select * from alert where num='%s'" % (s['sowid'])
        a=pd.read_sql(sqlcmd,con)
        quary_results=len(a)
        if quary_results == 0:
            sql = "insert into alert(num,smallpig,expectant,flag) values (\"%s\",'%s','%s','%s')"
            sql1 = sql % (s['sowid'], s['piglets'],s['detect_time'],'True')
            cur.execute(sql1)
            con.commit()
            print("新数据插入成功"+'\n')
        else:
            sql2="update alert set smallpig='%s',expectant='%s' where num='%s'" % (s['piglets'],s['detect_time'],s['sowid'])
            cur.execute(sql2)
            con.commit()
            print("已有数据更新成功")
    cur.close()
    con.close()

if __name__=='__main__':
    try:
        import_data('/home/promise/delivery_detect/output/piglet_detect.txt')
    except:
        print("暂无仔猪出生，没有写入数据库")
'''
con = pymysql.connect(host='127.0.0.1', port=3306, user='taimeng', password='meng', db='birth', charset='utf8')
sowid = 'A003003'
sqlcmd="select * from alert where num='%s'" % (sowid)
a=pd.read_sql(sqlcmd,con)
print(a)
'''
