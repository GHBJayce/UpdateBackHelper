# UpdateBackupHelper

更新备份助手，在你要对服务器的项目进行更新时，帮你把git commit中的最新文件、服务器项目的备份文件拷贝到本地指定目录，让你可以直接开始差异对比、合并差异的工作，最后上传更新到服务器。

## 使用
### 方式一
```shell
# 安装依赖
pip3 install gitpython
pip3 install paramiko
# 调用
py UpdateBackupHelper.py -c D:\config.json
```


### 方式二
直接运行[UpdateBackHelper.exe](https://github.com/GHBJayce/UpdateBackHelper/releases)
```shell
UpdateBackHelper.exe -c D:\config.json
```

## 配置文件说明
```jsonc
{
    "git": {
        "author": "GHBJayce", // 你在项目中的名称
        "last_commit_num": "5" // 项目最后5次的提交文件
    },
    // 本地配置
    "local": {
        "project_path": "F:\\you_project\\", // 本地项目路径
        "group": {
            "local_path": "E:\\update_backup\\", // 更新、备份文件路径
            "dir_list": ["backup", "new", "upload"] // backup备份、new最新文件、upload合并差异最终要上传的目录
        }
    },
    // 服务器配置
    "server": {
        "ip": "",
        "port": 22,
        "username": "root",
        "password": "",
        "project_path": "/root/you_project/" // 服务器项目路径
    }
}
```

## CHANGELOG

[CHANGELOG](./CHANGELOG.md)