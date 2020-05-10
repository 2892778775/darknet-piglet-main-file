import pymysql
import json
import datetime

def import_data(fn):
    # 读txt文件
    f = open(fn, 'r')
    m = f.readlines()

    con1 = pymysql.connect(host='127.0.0.1', port=3306, user='taimeng', password='meng', db='birth', charset='utf8')
    con2 = pymysql.connect(host='121.196.198.106',port=3306, user='root', password='123456', db='birth',charset='utf8')
    cur1 = con1.cursor()
    cur2 = con2.cursor()

    for line in m:
        A = line.strip('\n').split(',')
        A2 = []
        for a in A:
            b = a.strip(' ')
            A2.append(b)
        print(A2)
        s = {'sowid': A2[0],'frequency':int(A2[1]),'detect_time':A[2]}  # 转成字典
        #print("s:",s)
        #print("s[sowid]",s['sowid'])
        if len(A2)==3:
            sql = "insert into pre_alert(num,frequency,expectant) values (\"%s\",'%s','%s')"
            sql1 = sql % (s['sowid'], s['frequency'],s['detect_time'])
            cur1.execute(sql1)
            cur2.execute(sql1)
            con1.commit()
            con2.commit()
        else:
            sql2 = "insert into pre_alert(num,frequency,expectant,count) values (\"%s\",'%s','%s','%s')" % (s['sowid'], s['frequency'],s['detect_time'],A2[-1])
            cur1.execute(sql2)
            cur2.execute(sql2)
            con1.commit()
            con2.commit()
        print("写入数据库成功")


    cur1.close()
    cur2.close()
    con1.close()
    con2.close()

if __name__=='__main__':
    try:
        import_data('/home/promise/delivery_detect/output/posture_transition.txt')
        one_hour_before = datetime.datetime.now()-datetime.timedelta(hours=1)
        one_hour_now = datetime.datetime.now()
        print('已将%s到%s检测到的母猪姿态转化频率写入数据库'%(one_hour_before,one_hour_now))
    except:
        print("尚未检测到姿态变化")
