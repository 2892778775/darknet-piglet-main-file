import pymysql
import json
import pandas as pd
import time

def import_data(fn):
    # 读txt文件
    f = open(fn, 'r')
    m = f.readlines()
    print("检测到{0}条记录".format(len(m)))
    # 本地服务器
    con1 = pymysql.connect(host='127.0.0.1', port=3306, user='taimeng', password='meng', db='birth', charset='utf8')
    print('成功连接本地服务器!')
    # 阿里云服务器
    con2 = pymysql.connect(host='121.196.198.106',port=3306, user='root', password='123456', db='birth',charset='utf8')
    print('成功连接阿里云服务器!')
    cur1 = con1.cursor()
    cur2 = con2.cursor()
    # 将检测结果处理成数据库标准格式
    for line in m:
        A = line.strip('\n').split(',')
        A2 = []
        for a in A:
            b = a.strip(' ')
            A2.append(b)
        s = {'sowid': A2[0],'piglets':int(A2[1]),'detect_time':A[2]}  # 转成字典:栏位编号\仔猪数量\检测时间
        print("{0}号母猪分娩时间为{1}".format(s['sowid'],s['detect_time']))
        # 检查数据库中是否已经有了检测到的母猪信息
        sqlcmd1="select * from alert where num='%s'" % (s['sowid'])
        sqlcmd2="select smallpig from alert where num='%s'" % (s['sowid'])
        a=pd.read_sql(sqlcmd1,con1)
        b=pd.read_sql(sqlcmd2,con1)
        quary_results=len(a)
        # 如果没有现检测到的母猪信息, 插入检测信息
        if quary_results == 0:
            print('现将{0}号母猪分娩信息写入数据库'.format(s['sowid']))
            sql = "insert into alert(num,smallpig,expectant,flag, length, expectantone) values ('%s','%s','%s','%s','%s','%s')"
            sql1 = sql % (s['sowid'], s['piglets'],s['detect_time'],'True', 0, s['detect_time'])
            cur1.execute(sql1)
            cur2.execute(sql1)
            con1.commit()
            con2.commit()
            print("{0}号母猪分娩信息插入成功".format(s['sowid']))
        # 如果已经包含现检测到的母猪信息,比较仔猪数量,仔猪增加更新信息
        elif s['piglets'] >= b['smallpig'][0]:
            # 查询开始分娩时间
            print("{0}号母猪现已分娩{1}头仔猪".format(s['sowid'], s['piglets']))
            sql_start_time="select expectantone from alert where num='%s'" % (s['sowid'])
            # 获取开始分娩时间:字符串格式
            smallpigs_select=pd.read_sql(sql_start_time,con1)
            first_piglet_born_time = smallpigs_select.expectantone.values[0]
            fmt = '%Y-%m-%d %H:%M:%S'
            # 将开始分娩时间转化为时间戳(精确到秒)
            time1 = time.strptime(first_piglet_born_time, fmt)
            start_time = time.mktime(time1)
            delivery_time_now = s['detect_time']
            time2 = time.strptime(delivery_time_now, fmt) 
            end_time = time.mktime(time2)
            # 计算分娩时长
            delivery_length = end_time-start_time
            print("{0}号母猪现分娩时长为{1}".format(s['sowid'], delivery_length))
            sql2="update alert set smallpig='%s',expectant='%s',length='%s' where num='%s'" % (s['piglets'],s['detect_time'],delivery_length,s['sowid'])
            cur1.execute(sql2)
            cur2.execute(sql2)
            con1.commit()
            con2.commit()
            print("已有数据更新成功,现检测%s母猪在%s已分娩%s头仔猪" % (s['sowid'],s['detect_time'],b['smallpig'][0]))
        else:
            continue
    cur1.close()
    cur2.close()
    con1.close()
    con2.close()

if __name__=='__main__':
    #try:
    import_data('/home/promise/delivery_detect/output/piglet_detect.txt')
    #except:
        #print("暂无仔猪出生，没有写入数据库")
