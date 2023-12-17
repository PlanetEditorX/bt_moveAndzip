import sys
import re
import os
import shutil
import zipfile
import json
from pathlib import Path


# 适用格式 [作品类型(作者)]


def add_meta(path):
	# 拆分目录
	path_nums = path.split("\\")

	# 待修改文件夹名字
	name = path_nums.pop()

	# 拼接为所在父目录
	father_path = "\\".join(path_nums)
	print("name=", name)


	# 如果是zip文件
	if (os.path.splitext(name)[-1].lower() == '.zip'):
		meta = read_zip_file(path)

    # 未从压缩包中获取元数据
	if (meta == ''):
		unzip_file(path, father_path)

	return

# 压缩文件夹
# path 要压缩的文件夹具体路径


def zip_file(path):
	if not os.path.exists(path+".zip"):
		shutil.make_archive(path, 'zip', path)
	else:
		print(path+".zip is exist!")
	# 递归删除文件夹
	shutil.rmtree(path)
	return

# 读取zip文件
# path 压缩包具体地址
def read_zip_file(path):
	print(path, " is zip file")
	try:
		with zipfile.ZipFile(path, "r") as zip_ref:
			with zip_ref.open("info.json") as info:
				conObject = json.loads(info.read().decode('utf-8'))['gallery_info']
		# 获取元数据
		meta = conObject
	# 未获取到变量
	except KeyError:
		print("This ZIP file (" + path + ") does not contain metadata")
		meta = ''
	return meta

# 解压zip文件
def unzip_file(path, father_path):
	print(path, " is zip file")
	try:
		# 待解压文件夹
		folder_name = path.split(".zip")[0]
		with zipfile.ZipFile(path, 'r') as f:
			for fn in f.namelist():
				extracted_path = Path(f.extract(fn))
				extracted_path.rename(fn.encode('cp437').decode('gbk'))



		# zip_file = zipfile.ZipFile(path)
		# zip_list = zip_file.namelist() # 得到压缩包里所有文件

		# for f in zip_list:
		# 	zip_file.extract(f, folder_name)  # 循环解压文件到指定目录

		# zip_file.close()  # 关闭文件，必须有，释放内存


	# 未获取到变量
	# except KeyError:
	# 	print("This ZIP file (" + path + ") does not contain author information")
	# 	author = ''
	finally
	return



# 为当前目录下的zip文件添加元数据
folder_list = os.listdir(os.getcwd())
for folder_item in folder_list:
	if (os.path.splitext(folder_item)[-1].lower() == '.zip'):
		add_meta(os.getcwd() + "\\" + folder_item)
