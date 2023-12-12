import sys
import re
import os
import shutil

# 适用格式 [作品类型(作者)]
def move_folder(path):
	# 拆分目录
	path_nums = path.split("\\")

	# 待修改文件夹名字
	name = path_nums.pop()

	# 拼接为所在父目录
	father_path = "\\".join(path_nums)
	print("name=",name)

	# 从path中正则提取[]中的类型作者信息
	if (re.search(r"(?<=\[)(.+?)(?=\])",name)): 

	elif ():
		type_author = re.search(r"(?<=\[)(.+?)(?=\])",name).group(0).strip()
	# print("type_author=",type_author)

	# 定义排除类型
	unexpect_type = ["中国翻訳","中国翻译","翻译","翻訳","DL版","DL"]

	# 未找到作者，格式不标准或本身未标注作者信息
	if ('(' in type_author and ')' in type_author):
		# 从类型作者中提取出()中作者信息
		author = re.search(r"(?<=\()(.+?)(?=\))",type_author).group(0).strip()
	# 仅有类型或仅有作者，以类型/作者分类,除去空格后只有字母和数字进入条件
	elif (type_author.replace(' ','').isalnum() and type_author not in unexpect_type):
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
	new_path = new_folder.strip() + '\\' + name

	if not os.path.exists(new_path):
		shutil.move(path, new_path)
		# print("Python move ",path," to ",new_path)
	else:
		print(new_path," is exist!")

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

if len(sys.argv) > 1:
	# 获取命令行参数
	move_folder(sys.argv[1])

else:
	# 直接运行移动当前目录下的文件夹
	folder_list = os.listdir(os.getcwd())
	for folder_item in folder_list:
		if ('[' in folder_item and ']' in folder_item or '【' in folder_item and '】' in folder_item):
			move_folder(os.getcwd() + "\\" + folder_item)

