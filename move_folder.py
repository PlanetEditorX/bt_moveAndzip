import sys
import re
import os
import shutil
import zipfile
import json
from datetime import datetime

# 适用格式 [作品类型(作者)]
def move_folder(path):
	# 拆分目录
	path_nums = path.split("\\")

	# 待修改文件夹名字
	name = path_nums.pop()

	# 拼接为所在父目录
	father_path = "\\".join(path_nums)
	print("name=",name)

	# 判断是否是zip文件
	flag_zip = 0
	# 作者名字
	author = ''
	type_author = ''
	# 如果是zip文件
	if (os.path.splitext(name)[-1].lower() == '.zip'):
		flag_zip = 1
		author = unzip_file(path)
	# 如果是cbz文件
	elif(os.path.splitext(name)[-1].lower() == '.cbz'):
		flag_zip = 2
		author = uncbz_file(path)

	# 如果未获取到作者信息
	if (author == ''):
		# 从path中正则提取[]中的类型作者信息
		if (re.search(r"(?<=\[)(.+?)(?=\])",name)):
			type_author = re.search(r"(?<=\[)(.+?)(?=\])", name).group(0).strip()
		elif (re.search(r"(?<=【)(.+?)(?=】)", name)):
			type_author = re.search(r"(?<=【)(.+?)(?=\】)",name).group(0).strip()

		# 定义排除类型
		unexpect_type = ["中国翻訳","中国翻译","翻译","翻訳","DL版","DL"]

		# 未找到作者，格式不标准或本身未标注作者信息
		if ('(' in type_author and ')' in type_author):
			# 从类型作者中提取出()中作者信息
			author = re.search(r"(?<=\()(.+?)(?=\))",type_author).group(0).strip()
		# 仅有类型或仅有作者，以类型/作者分类,除去空格后只有字母和数字进入条件
		# isalnum() 方法检测字符串是否由字母和数字组成,如果 string 至少有一个字符并且所有字符都是字母或数字则返回 True,否则返回 False
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
	# 创建移动后文件夹目录
	new_path = new_folder.strip() + '\\' + name
	if (flag_zip == 2):
		f_path = path.split(".cbz")[0]
		new_path = new_path.split(".cbz")[0]

	# 判断移动后目录是否存在
	if not os.path.exists(new_path):
		# 进行移动操作
		if (flag_zip == 0 or flag_zip == 1):
			shutil.move(path, new_path)
		elif (flag_zip == 2):
			# 删除cbz包
			os.remove(path)
			# 移动文件夹到作者目录下
			shutil.move(f_path, new_path.split(".cbz")[0])
	else:
		print(new_path," is exist!")

	# 如果不是zip文件
	if (flag_zip == 0 or flag_zip == 2):
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

# 解压zip文件，返回作者信息
# path：压缩包具体地址
def unzip_file(path):
	print(path, " is zip file")
	if contains_file(path, 'info.json'):
		author = get_form_info(path)
	elif contains_file(path, 'meta.json'):
		author = get_form_meta(path)
	else:
		author = ''
	return author

# 从info.json文件中获取数据
# path：压缩包具体地址
def get_form_info(path):
	try:
		with zipfile.ZipFile(path, "r") as zip_ref:
			with zip_ref.open("info.json") as info:
				conentObject = json.loads(info.read().decode('utf-8'))['gallery_info']
		# 获取作者英文信息，并单词首字母大写
		author = conentObject['tags']['artist'][0].title()
		if ("|" in author):
			# 多个作者信息时取第一项，并删除空格
			author = author.split("|")[0].replace(' ', '')
	# 未获取到变量
	except KeyError:
		print("This ZIP file (" + path + ") does not contain author information")
		author = ''
	# JSONDecodeError异常
	except json.decoder.JSONDecodeError as e:
		print("JSONDecodeError:", str(e))
		author = ''
	return author

# 从meta.json文件中获取数据
# path：压缩包具体地址
def get_form_meta(path):
	try:
		with zipfile.ZipFile(path, "r") as zip_ref:
			with zip_ref.open("meta.json") as info:
				conentObject = json.loads(info.read().decode('utf-8'))
		# 获取作者英文信息
		author = conentObject['tags']['artist'][0]
		add_Comicinfo(path, conentObject)
	# 未获取到变量
	except KeyError:
		print("This ZIP file (" + path + ") does not contain author information")
		author = ''
	# JSONDecodeError异常
	except json.decoder.JSONDecodeError as e:
		print("JSONDecodeError:", str(e))
		author = ''
	return author_format(author)

# 提取信息
def add_Comicinfo(path, obj):
	output = os.path.dirname(path)  # 当前目录文件夹
	comicinfo_exists(output) # 生成模板文件
	output_modelfile = output + '\\ComicInfo.xml'
	# 读取信息
	with open(output_modelfile, encoding = "utf-8") as file:
		content = file.read()

	# Title：000是英文，001是日文
	content = content.replace('$01', obj['originTitle'])
	# Notes：备注
	content = content.replace('$02', 'Created by Eh-View-Enhance (MapoMagpie/eh-view-enhance)')
	content = content.replace('$03', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	# 日期处理：该插件并无日期元数据
	# Year：年份
	content = content.replace('$04','')
	# Month：月份
	content = content.replace('$05', '')
	# Day：天
	content = content.replace('$06', '')
	# Writer：作者
	content = content.replace('$07', obj['tags']['artist'][0].title())
	# Tags：标签
	content = content.replace('$08', list_str(obj['tags'], ['language','parody','character','group','male','female','other']))
	# Web：网页
	content = content.replace('$09', obj['url'])
	# PageCount：页数
	content = content.replace('$10', str(get_files_from_zip(path)))
	# LanguageISO：语言
	content = content.replace('$11', 'zh')
	# Format：格式
	content = content.replace('$12', 'Digital')
	# Manga：管理
	content = content.replace('$13', 'Yes')
	# Characters：分类
	content = content.replace('$14', list_str(obj['tags'], ['character']))
	# 写入文件
	with open(output_modelfile,"w",encoding="utf-8") as f:
		f.write(content)

	# 向ZIP文件中添加文件
	with zipfile.ZipFile(path, 'a', zipfile.ZIP_DEFLATED) as zipf:
		zipf.write(output_modelfile, arcname='ComicInfo.xml')

	# 删除生成的模板文件
	del_modelfile(output_modelfile)
	return

# 指定数组转字符串
def list_str(obj, _list):
	"""
	指定数组转字符串
	:param obj: 原始对象
    :param _list: 需要获取的属性数组
	"""
	content = ''
	for key in obj:
		if key in _list:
			content += ','.join([str(x) for x in obj[key]]) + ','

	return content[:-1]

# 获取压缩包文件数量
def get_files_from_zip(zip_file_path):
	file_list = []
	with zipfile.ZipFile(zip_file_path, 'r') as z:
		file_list = z.namelist()
	# 去除数据，只保留图片计算数量
	file_list.remove('meta.json')
	return len(file_list)

# 判断压缩包是否包含指定文件
# zip_path：压缩包路径
# filename：文件名字
def contains_file(zip_path, filename):
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            return filename in z.namelist()
    except zipfile.BadZipFile:
        return False

# 解压cbz文件
# path 压缩包具体地址
def uncbz_file(path):
	print(path, " is cbz file")
	try:
		newFolder = path.split(".cbz")[0]
		# 解压cbz文件，默认插件下载的格式为xxx.cbz/xxxx/01.jpg
		zip = zipfile.ZipFile(path)
		folderName = zip.namelist()[0].split("/")[0] # 非标准文件夹名字
		output = os.path.dirname(path)  # 默认解压到当前目录同名文件夹中
		zip.extractall(output)   # 会被解压到输入的路径中
		zip.close()
		# 重命名为标准文件夹名
		os.rename(output + '\\' + folderName, newFolder)
		# 复制ComicInfo.xml模板
		comicinfo_exists(newFolder)
		# 读取信息
		with open(newFolder + '\\ComicInfo.xml', encoding = "utf-8") as file:
			content = file.read()

		with open(newFolder + '\\info.txt', 'r',  encoding = "utf-8") as f:
			lines = f.readlines()
			# Title：000是英文，001是日文
			content = content.replace('$01', lines[1][:-1])
			# Notes：备注
			content = content.replace('$02', 'Created by E-Hentai Downloader (ccloli/E-Hentai-Downloader)')
			content = content.replace('$03', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			# 日期处理 保留XXXX-XX-XX
			fileTime = lines[6][8:-7].split('-')
			# Year：年份
			content = content.replace('$04', fileTime[0])
			# Month：月份
			content = content.replace('$05', fileTime[1])
			# Day：天
			content = content.replace('$06', fileTime[2])
			# Writer：作者
			author = str_tag(lines, 0)
			content = content.replace('$07', author)
			# Tags：标签
			content = content.replace('$08', str_tag(lines, 1))
			# Web：网页
			content = content.replace('$09', lines[2][:-1])
			# PageCount：页数
			content = content.replace('$10', re.findall(r'\d+', lines[11])[0])
			# LanguageISO：语言
			content = content.replace('$11', 'zh')
			# Format：格式
			content = content.replace('$12', 'Digital')
			# Manga：管理
			content = content.replace('$13', 'Yes')
			# Characters：分类
			content = content.replace('$14', lines[4][10:-1])

		with open(newFolder + '\\ComicInfo.xml',"w",encoding="utf-8") as f:
			f.write(content)

	# 未获取到变量
	except KeyError:
		print("This CBZ file (" + path + ") does not contain author information")
		author = ''
	# JSONDecodeError异常
	except json.decoder.JSONDecodeError as e:
		print("JSONDecodeError:", str(e))
		author = ''
	# 未找到文件
	except FileNotFoundError:
		print("This file not found")
		author = ''
	return author_format(author)

# 作者仅保留一项,并大写首字母
def author_format(author):
	if ("|" in author):
		# 多个作者信息时取第一项，并删除空格
		author = author.split("|")[0].strip()
	elif ("," in author):
		author = author.split(",")[0].strip()
	return author.title()

# 标签处理
def str_tag(lines, index):
	content = ''
	flag = 0
	for line in lines:
		if flag == 1 and '>' in line:
			content = content + line.split(':')[1][:-1].strip() + ','
			# 返回作者
			if index == 0 and 'artist' in line:
				return line[10:-1].title()

		elif re.search('Tags:', line):
			flag = 1
		else:
			flag = 0
			if not len(content) == 0:
				break
	return content[:-1]

# 模板文件是否存在
def comicinfo_exists(path):
	modulefile_path = os.path.dirname(os.path.realpath(__file__)) + '\\model\\ComicInfo.xml'
	comicinfo_path = path + '\\ComicInfo.xml'
	if not os.path.exists(comicinfo_path):
		shutil.copy(modulefile_path, path)
	return

# 删除模板文件
def del_modelfile(path):
	# 删除生成的模板文件
	if os.path.exists(path):
		print(f"删除模板文件{path}")
		print(f"{path}删除成功")
		os.remove(path)

if len(sys.argv) > 1:
	# 获取命令行参数
	move_folder(sys.argv[1])

else:
	# 直接运行移动当前目录下的文件夹
	root_path = os.getcwd()
	print(f"运行目录为：{root_path}")
	folder_list = os.listdir(root_path)
	for folder_item in folder_list:
		if ('[' in folder_item and ']' in folder_item or '【' in folder_item and '】' in folder_item or os.path.splitext(folder_item)[-1].lower() == '.zip'):
			move_folder(os.getcwd() + "\\" + folder_item)
	del_modelfile(f"{root_path}\\ComicInfo.xml")
