#-*- coding:utf-8 -*-
import json
from git import Repo
import os
import shutil
import datetime
import paramiko
import sys

if len(sys.argv) < 2:
    print('请传入json配置文件')
    quit()

config_json_file_path = sys.argv[1]

if not config_json_file_path.lower().endswith('json'):
    print('请传入正确的json文件')
    quit()

if not os.path.exists(config_json_file_path):
    print('无效路径，配置文件不存在')
    quit()

def loadConfig(file_path):
    file = open(file_path, encoding='utf-8')

    return json.load(file)

config = loadConfig(config_json_file_path)

repo = Repo(config['local']['project_path'])
#heads = repo.heads
#master = heads.master

# print(config)

# print(master.log())

git = repo.git
git_log_result = git.log('--name-only', '--no-merges', '-' + config['git']['last_commit_num'], '--author=' + config['git']['author'], '--pretty=format:')
# print(git_log_result)

file_list = git_log_result.strip("\n").replace("\n\n", "\n").split("\n") # 去除首尾换行、处理双换行、按照换行组合成数组
# 去重 保留原有顺序
file_list_handle = []
for v in file_list:
    if v not in file_list_handle:
        file_list_handle.append(v)
# print(file_list_handle)

for i in file_list_handle:
    print("\n", str(file_list_handle.index(i)) + '.', i, "\n")

user_input_result = input('按照序号选择你要处理的文件，多个文件使用空格隔开，选择全部可以直接输入all : ')
if user_input_result.strip() == '':
    print('输入为空，取消操作')
    exit()
elif user_input_result == 'all':
    user_choose_result = [file_list_handle.index(v) for v in file_list_handle]
else:
    user_choose_result = user_input_result.strip().split()
# print(user_choose_result)

final_file_list = []
for num in user_choose_result:
    if int(num) > len(file_list_handle) - 1:
        print('序号不存在，请输入正确的序号再试')
        quit()
    else:
        final_file_list.append(file_list_handle[int(num)])

# print(final_file_list)



def create_directory_path(path):
    if os.path.exists(path) is False:
        os.makedirs(path)

# 创建本地备份目录
local_project_path = config['local']['project_path']
local_group_dir_name = format(datetime.datetime.now().strftime('%Y-%m-%d %H_%M_%S'))
local_group_dir_path = config['local']['group']['local_path'] + local_group_dir_name + '/'

create_directory_path(local_group_dir_path)

# 创建本地备份三大目录
# backup: 服务器的备份
# new: 用来存放最新的文件
# upload: 用于存放（在比较差异合并差异之后）确认上传的文件
for v in config['local']['group']['dir_list']:
    create_directory_path(local_group_dir_path + v)

local_new_dir_path = local_group_dir_path + 'new/'
local_backup_dir_path = local_group_dir_path + 'backup/'
local_upload_dir_path = local_group_dir_path + 'upload/'


def getServerSftp(server_info):
    scp = paramiko.Transport((server_info['ip'], server_info['port']))
    scp.connect(username=server_info['username'], password=server_info['password'])

    return paramiko.SFTPClient.from_transport(scp)

sftp = getServerSftp(config['server'])
server_project_path = config['server']['project_path']


print("\n\n正在创建此次拷贝清单files.txt")
files_resource = open(local_group_dir_path + 'files.txt', 'a')
for v in final_file_list:
    files_resource.write(v + "\n")
files_resource.close()
print("\n\n创建成功")

print("\n\n正在拷贝最新文件到new目录")
for v in final_file_list:
    # 拷贝最新文件
    origin_file = local_project_path + v
    to_file = local_new_dir_path + v

    # 2019-1-15 若commit中有新增、删除文件
    if os.path.exists(origin_file) is True:
        create_directory_path(os.path.dirname(to_file))

        shutil.copy(origin_file, to_file)
        print("\033[1;36m%s\033[0m 到 \033[1;32m%s\033[0m \n拷贝成功" %(origin_file, to_file))
        # print("\n", '拷贝成功', origin_file, '到', to_file)


print("\n\n正在拷贝服务器备份到backup目录")
for v in final_file_list:
    # 拷贝服务器备份
    origin_file = server_project_path + v
    to_file = local_backup_dir_path + v

    # 2019-1-15 若commit中有新增、删除文件，服务器不存在文件会出现错误，这里捕获这个错误反馈给用户，并让程序走下去
    try:
        create_directory_path(os.path.dirname(to_file))

        sftp.get(origin_file, to_file)
        print("\033[1;35m%s\033[0m 到 \033[1;32m%s\033[0m \n拷贝成功" %(origin_file, to_file))
    except Exception as e:
        print('该文件可能是删除或新增的文件，所以无法拷贝；错误内容：', e)


print("\n\n再拷一份服务器备份到upload目录")
for v in final_file_list:
    # 再拷一份到upload
    origin_file = server_project_path + v
    to_file = local_upload_dir_path + v

    # 2019-1-15 若commit中有新增、删除文件，服务器不存在文件会出现错误，这里捕获这个错误反馈给用户，并让程序走下去
    try:
        create_directory_path(os.path.dirname(to_file))

        sftp.get(origin_file, to_file)
        print("\033[1;34m%s\033[0m 到 \033[1;32m%s\033[0m \n拷贝成功" %(origin_file, to_file))
    except Exception as e:
        print('该文件可能是删除或新增的文件，所以无法拷贝；错误内容：', e)