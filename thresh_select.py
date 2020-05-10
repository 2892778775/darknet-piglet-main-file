import os
import glob
import time

path1 = '/home/promise/anaconda3/envs/tf-gpu/darknet/results'
path2 = '/home/promise/delivery_detect/postures_detect'
file1 = '/home/promise/anaconda3/envs/tf-gpu/darknet/results/postures.txt'
file2 = '/home/promise/anaconda3/envs/tf-gpu/darknet/results/sort.txt'
file3 = '/home/promise/anaconda3/envs/tf-gpu/darknet/results/posture_transition.txt'
file4 = '/home/promise/anaconda3/envs/tf-gpu/darknet/results/postures_detection.txt'

#try:
#创建sowid：posture(每一帧对应一条记录)，筛选置信度
for file in os.listdir(path1):
	filename = file.split('.')[0]
	posture = filename.split('_')[1]
	with open(os.path.join(path1,file), 'r') as fr:
		for line in fr.readlines():
			picname = line.strip().split(' ')[0]
			thresh = line.strip().split(' ')[1]
			if float(thresh) > 0.6:
				with open(file1, 'a') as fa:
					fa.write(picname+','+posture+'\n')

#图像排序
with open(file1,'r') as fr:
	postures=[]
	for line in fr.readlines():
		if line not in postures:#如果一张图像有多个置信度阈值超过0.6的预测结果，则随机选择一个
			postures.append(line)
sort_postures = sorted(postures)
with open(file2,'a') as fa:
	for i in range(len(sort_postures)):
		fa.write(sort_postures[i])

#输出sowid:postures transitions times格式文件
postures_list = {}
with open(file2,'r') as fr:
	for line in fr.readlines():
		line = line.strip()
		sowid = line.split('_')[0]
		posture = line.split(',')[1]
		if sowid not in postures_list.keys():
			postures_list[sowid] = [posture]
		else:
			postures_list[sowid].append(posture)

for key in postures_list.keys():
	a = 1
	for i in range(len(postures_list[key])-1):
		beforepic = postures_list[key][i]
		nextpic = postures_list[key][i+1]
		if beforepic == nextpic:
			continue
		else:
			a += 1
	postures_list[key] = a
		

for key in postures_list.keys():
	with open(file3, 'a') as fa:
		fa.write(key + ',' + str(postures_list[key])+','+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')

with open(file3,'r') as fr:
	lines = fr.readlines()
	#line_list = lines.strip().split(' ')
	calculate_line = len(lines)-1
	print(calculate_line)
	with open(file4, 'a') as fa:
		for num,content in enumerate(lines):
			print(num,content)
			if num == calculate_line:
				fa.write(content.strip()+','+str(num+1))
			else:
				fa.write(content)

os.remove(file1)
os.remove(file2)

