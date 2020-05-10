import shutil 
import os
import glob
import time

file1 = '/home/promise/darknet/warning.txt'
file2 = '/home/promise/delivery_detect/output/detect_piglet_pic.txt'
file3 = '/home/promise/delivery_detect/output/piglet_detect.txt'
dir1 = '/home/promise/delivery_detect/output/images'
dir2 = '/home/promise/delivery_detect/output/piglet'
dir3 = '/home/promise/delivery_detect/output/labels'


#选择检测到仔猪结果的图像,将图像名称存储到file2 (O(n))
with open (file1,'r') as fr:
	for line in fr.readlines():
		keyword = line.strip().split(' ')[0]
		#for line in fr.readlines():
		if keyword == 'saved':
			picname = line.strip().split('/')[-1]
			with open(file2, 'a') as fa:
				fa.write(picname[:-4]+'\n')

#去重复
try:
	picname = {}
	with open(file2, 'r') as fr:
		for line in fr.readlines():
			#sowid = line.strip().split('_')[0]
			picid = line.strip()
			if picid not in picname.keys():
				picname[picid]=1
			else:
				picname[picid] += 1#每一张图片建立一个key-value，不是每一只猪建立一个key-value
	# 同时检测一头母猪的多张图像,选择仔猪数量最多的一张为检测结果
	select_max_piglets_num ={}
	for key in picname.keys():
		sowid = key.split('_')[0]
		max_piglets_num = picname[key]
		#max_piglets_num = piglets_num
		if sowid not in select_max_piglets_num.keys():
			select_max_piglets_num[sowid] = max_piglets_num
		elif max_piglets_num > select_max_piglets_num[sowid]:
			select_max_piglets_num[sowid] = max_piglets_num
		
	with open(file3, 'a') as fa:
		for key in select_max_piglets_num.keys():
			fa.write(key+ ',' + str(select_max_piglets_num[key]) +','+time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'\n')

#将含有仔猪的图像转移到另一个文件夹，将没有检测到仔猪的图像删除，同时删除检测结果
	with open(file2,'r') as fr2:
		for line in fr2.readlines():
			for picname in os.listdir(dir1):
				if picname[:-4] == line.strip():
					shutil.move(os.path.join(dir1,picname), dir2)

except:
	print("暂无仔猪出生")
	pass	
				
			




