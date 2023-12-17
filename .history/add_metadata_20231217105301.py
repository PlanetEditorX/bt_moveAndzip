import sys
import re
import os
import shutil
import zipfile
import json

# 适用格式 [作品类型(作者)]


def move_folder(path):
	# 拆分目录
	path_nums = path.split("\\")

	# 待修改文件夹名字
	name = path_nums.pop()

	# 拼接为所在父目录
	father_path = "\\".join(path_nums)
	print("name=", name)

	# 判断是否是zip文件
	flag_zip = 0
	# 作者名字
	author = ''
	type_author = ''
	# 如果是zip文件
	if (os.path.splitext(name)[-1].lower() == '.zip'):
		flag_zip = 1
		author = unzip_file(path)
	# 如果未获取到作者信息
	if (author == ''):
		# 从path中正则提取[]中的类型作者信息
		if (re.search(r"(?<=\[)(.+?)(?=\])", name)):
			type_author = re.search(r"(?<=\[)(.+?)(?=\])", name).group(0).strip()
		elif (re.search(r"(?<=【)(.+?)(?=】)", name)):
			type_author = re.search(r"(?<=【)(.+?)(?=\】)", name).group(0).strip()

		# 定义排除类型
		unexpect_type = ["中国翻訳", "中国翻译", "翻译", "翻訳", "DL版", "DL"]

		# 未找到作者，格式不标准或本身未标注作者信息
		if ('(' in type_author and ')' in type_author):
			# 从类型作者中提取出()中作者信息
			author = re.search(r"(?<=\()(.+?)(?=\))", type_author).group(0).strip()
		# 仅有类型或仅有作者，以类型/作者分类,除去空格后只有字母和数字进入条件
		# isalnum() 方法检测字符串是否由字母和数字组成,如果 string 至少有一个字符并且所有字符都是字母或数字则返回 True,否则返回 False
		elif (type_author.replace(' ', '').isalnum() and type_author not in unexpect_type):
			author = type_author
		# 其它情况
		else:
			author = "Other"

	# 需要创建的作者目录
	new_folder = father_path + '\\' + author

	# 判断文件夹是否存在
	if not os.path.exists(new_folder):
		# 创建文件夹
		os.mkdir(new_folder)

	# 移动文件夹到作者目录下
	# 创建移动后文件夹目录
	new_path = new_folder.strip() + '\\' + name
	# 判断移动后目录是否存在
	if not os.path.exists(new_path):
		# 进行移动操作
		shutil.move(path, new_path)
		# print("Python move ",path," to ",new_path)
	else:
		print(new_path, " is exist!")

	# 如果不是zip文件
	if (flag_zip == 0):
		zip_file(new_path)
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


if len(sys.argv) > 1:
	# 获取命令行参数
	move_folder(sys.argv[1])

else:
	# 为当前目录下的zip文件添加元数据
	folder_list = os.listdir(os.getcwd())
	for folder_item in folder_list:
		if (os.path.splitext(folder_item)[-1].lower() == '.zip'):
			move_folder(os.getcwd() + "\\" + folder_item)
