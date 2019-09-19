
# CHANGELOG

## version 1.2

- 检测抛出配置文件中路径配置项结尾缺失`/`的提示语
- 更改配置文件传入的方式，现在传入配置文件路径需要在前面增加`-c`或者`--config`

    ```shell
    UpdateBackupHelper.exe -c=./config.json # 第一种方式
    UpdateBackupHelper.exe -c ./config.json # 第二种方式
    ```

- 另外，新增两个传入参数，优先级高于配置文件中的配置项，分别是`last_commit_num`、`author`配置项

    - `last_commit_num` 最后提交的git次数，`-q`或者`--quantity`
    - `author` 提交的git作者，`-a`或者`--author`

    ```shell
    UpdateBackupHelper.exe -c ./config.json -a GHBJayce -q 6 # 第二种方式
    ```

## version 1.1

- [x] 拷贝不存在（新增/删除）的文件时，使用捕获异常并给出提示的方式告知用户
- [x] 配置文件的引入方式，改换以参数（配置文件路径）形式传递

    > 原方式：固定一个`config.json`文件，且必须同程序一个目录，当多个项目需要使用时，切换比较困难，不够灵活
    > 现：灵活应用于多个项目之间切换，且不限制配置文件的名称、所在位置，只要是`json`文件即可

- [x] 验证配置文件参数必填，且为有效（能打开）的json文件