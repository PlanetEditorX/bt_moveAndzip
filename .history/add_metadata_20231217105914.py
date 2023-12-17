import sys
import re
import os
import shutil
import zipfile
import json

# 适用格式 [作品类型(作者)]


def add_meta(path):
	# 拆分目录
	path_nums = path.split("\\")

	# 待修改文件夹名字
	name = path_nums.pop()

	# 拼接为所在父目录
	print("name=", name)

	# 如果是zip文件
	if (os.path.splitext(name)[-1].lower() == '.zip'):
		author = unzip_file(path)

	if (author == ''):
		author = unzip_file(path)

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

# 解压zip文件
# path 压缩包具体地址


def unzip_file(path):
	print(path, " is zip file")
	try:
		with zipfile.ZipFile(path, "r") as zip_ref:
			with zip_ref.open("info.json") as info:
				conObject = json.loads(info.read().decode('utf-8'))['gallery_info']
		# 获取作者英文信息，并单词首字母大写
		author = conObject['tags']['artist'][0].title()
		if ("|" in author):
			# 多个作者信息时取第一项，并删除空格
			author = author.split("|")[0].replace(' ', '')
	# 未获取到变量
	except KeyError:
		print("This ZIP file (" + path + ") does not contain author information")
		author = ''
	return author



# 为当前目录下的zip文件添加元数据
folder_list = os.listdir(os.getcwd())
for folder_item in folder_list:
	if (os.path.splitext(folder_item)[-1].lower() == '.zip'):
		add_meta(os.getcwd() + "\\" + folder_item)
