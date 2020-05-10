import pymysql
import json
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
        print(A2)
        s = {'sowid': A2[0],'piglets':int(A2[1]),'detect_time':A[2]}  # 转成字典
        print("s:",s)
        print("s[sowid]",s['sowid'])
        sql = "insert into alert(num,smallpig,expectant) values (\"%s\",'%s','%s')"
        sql1 = sql % (s['sowid'], s['piglets'],s['detect_time'])
        print("写入数据库成功")
        cur.execute(sql1)
        con.commit()

    cur.close()
    con.close()

if __name__=='__main__':
    #try:
    import_data('/home/promise/delivery_detect/output/piglet_detect.txt')
    #except:
        #print("暂无仔猪出生，没有写入数据库")
