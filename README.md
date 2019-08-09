
##### 一个简单易用的 request 模拟工具（py3）

![image](https://raw.githubusercontent.com/cilame/vrequest/master/test/show.png)

```
带有简单的代码生成功能（能生成 scrapy 或 requests 的请求代码）
带有方便的记录配置的功能（持久化请求配置内容，方便以后使用）
带有多种加解密样例，加解密功能丰富。（大部分加解密都有纯py算法展示，更少的第三方依赖）
```

![image](https://raw.githubusercontent.com/cilame/vrequest/master/test/show2.jpg)

- ##### 安装方式/依赖

```bash
# 安装方式，通过pip安装即可
C:\Users\zhoulin08>pip install vrequest
# 通过git+pip进行安装
C:\Users\zhoulin08>pip install git+https://github.com/cilame/vrequest.git
# 下载安装该库会自动依赖安装 requests, lxml 这两个库
# 其他的依赖不会主动安装，因为与请求功能没有强耦合要求。所以会在那些功能被使用的时候提示没有该库
# 额外的依赖和功能：
# pyexecjs 或 js2py 任选其一，用于测试执行 js 脚本
# jsbeautifier      用于结构化 js 脚本
# cryptography      用于一些比较小众且我很难找得到的算法加解密

# 另外，如果你只想要使用加解密功能的话，你可以增加 --no-deps 的pip下载配置避免依赖下载，因为加解密部分的功能，
# 只要工具内没有明说存在依赖，就代表那些解密的功能全部都由不需要依赖，都有单个脚本直接实现。
# 甚至二维码的加解密都将依赖库都压缩着包含在了单个脚本内部。
C:\Users\zhoulin08>pip install vrequest --no-deps
```

- ##### 打开方式

```bash
# 在安装该函数库后就有一个命令行工具，直接在命令行输入 vv 或者 vrequest 都可以打开该GUI工具
# eg.
C:\Users\zhoulin08>vv
# 并且功能描述都有写在帮助页，直接按照帮助页中的各种快捷键处理方式就可以
# 0 该工具大部分都是快捷键操作
# 1 可以将请求过的数据记录在本地，并且可以更新配置
#   哪怕关掉工具也能很方便的恢复请求的配置状态，方便使用
# 2 快速生成请求代码，让请求更加方便实现。
# ps.
C:\Users\zhoulin08>ee
# 在输入参数中加上e则会直接打开便捷加密窗口，或者输入 vv e 也可以打开，这里重复是为了防止与其他工具冲突，
# 不用再工具里右键打开
```


