'''
将画面截取文件夹下的图片绝对路径写入txt文件
'''

import os
import shutil
 
path = '/home/promise/delivery_detect/input_split'
new_path = '/home/promise/delivery_detect/piglet_detect'
 
def get_filelist_to_txtfile(dir):
    Filelist=[]
    for home, dirs, files in os.walk(path):
        for filename in files:
            root = os.path.join(home, filename)
            shutil.copy(root, new_path+'/')
            Filelist.append(root)
#    with open(txtfile,'a')as fa:
#        for i in Filelist:        
#            fa.write(i+'\n')
    return Filelist
 
if __name__ =="__main__":
    Filelist = get_filelist_to_txtfile(path)
    print(len(Filelist))

	
