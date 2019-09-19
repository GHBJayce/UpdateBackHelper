# UpdateBackupHelper

更新备份助手，在你要对服务器项目更新之前，自动帮你把最新文件和备份文件拷贝到指定目录，让你可以直接开始差异对比、合并差异的工作。节省时间

## 使用

调用说明：

程序 json配置文件的路径


### 方式一

命令行工具中执行

```shell
py UpdateBackupHelper.py -c D:\config.json
```


### 方式二

直接运行`UpdateBackHelper.exe`

[下载exe](https://github.com/GHBJayce/UpdateBackHelper/releases)


### 方式三

命令行工具中执行，进入程序所在目录下

```shell
UpdateBackHelper.exe -c D:\config.json
```


## 配置文件说明
```
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