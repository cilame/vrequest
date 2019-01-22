
##### 一个简单易用的 request 模拟工具

```
带有简单的代码生成功能（快速测试需求）
带有方便的记录配置的功能（持久化请求配置内容，方便以后使用）
```

- ##### 安装方式/依赖

```bash
# 安装方式，通过pip安装即可
C:\Users\zhoulin08>pip install vrequest
# 通过git+pip进行安装
C:\Users\zhoulin08>pip install git+https://github.com/cilame/vrequest.git
# 下载安装该库会自动依赖安装 requests, lxml 这两个库
```

- ##### 打开方式

```bash
# 在安装该函数库后就有一个命令行工具，直接在命令行输入 vv 即可打开该GUI工具
# eg.
C:\Users\zhoulin08>vv
# 并且功能描述都有写在帮助页，直接按照帮助页中的各种快捷键处理方式就可以
# 0 该工具大部分都是快捷键操作
# 1 可以将请求过的数据记录在本地，并且可以更新配置
#   哪怕关掉工具也能很方便的恢复请求的配置状态，方便使用
# 2 快速生成请求代码，让请求更加方便实现。
```