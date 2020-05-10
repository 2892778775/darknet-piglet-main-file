import os 

path = '/mnt/NAS139/b307'

filenames = os.listdir(path)

while not filenames:
	print("未检测到摄像头截取图像,仍在监听中....")
	filenames = os.listdir(path)
print('现已检测到摄像头图像, 开始调用检测模型')

