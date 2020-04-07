# -*- coding: utf-8 -*-

# Scrapy settings for v project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'v'

SPIDER_MODULES = ['v.spiders']
NEWSPIDER_MODULE = 'v.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'v (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False # 几乎用不到的功能默认关闭，提高任务执行效率

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

IMAGES_STORE = 'image' # 默认在该脚本路径下创建文件夹、下载图片(不解开 VImagePipeline 管道注释则该配置无效)
FILES_STORE = 'file'   # 默认在该脚本路径下创建文件夹、下载文件(不解开 VFilePipeline 管道注释则该配置无效)
MEDIAS_STORE = 'media' # 默认在该脚本路径下创建文件夹、下载【媒体】(不解开 VVideoPipeline 管道注释则该配置无效)
ITEM_PIPELINES = {
    # 'v.pipelines.VPipeline':      101, # 普通的中间件使用(解开即可测试，如需魔改，请在脚本顶部找对应的类进行自定义处理)
    # 'v.pipelines.VImagePipeline': 102, # 图片下载中间件，item 带有 src 字段则以此作为图片地址下载到 IMAGES_STORE 地址的文件夹内
    # 'v.pipelines.VFilePipeline':  103, # 文件下载中间件，item 带有 src 字段则以此作为文件地址下载到 FILES_STORE 地址的文件夹内
    # 'v.pipelines.VVideoPipeline': 104, # 视频下载中间件，同上，以 src 作为下载地址，下载到当前路径下的 video 文件夹内
    # 'v.pipelines.VMySQLPipeline': 105, # MySql 插入中间件，具体请看类的描述
} 
SPIDER_MIDDLEWARES = { 
    # 'v.middlewares.VSpiderMiddleware': 543,     # 原版模板的单脚本插入方式
} 
DOWNLOADER_MIDDLEWARES = { 
    # 'v.middlewares.VDownloaderMiddleware': 543, # 原版模板的单脚本插入方式
    # 'v.middlewares.VSeleniumMiddleware': 544,   # 单脚本 Selenium 中间件配置，解开自动使用 Selenium，详细请看 VSeleniumMiddleware 类中间件代码。
}
EXTENSIONS = {
    # 'scrapy.extensions.logstats.LogStats': None, 
    # 关闭 scrapy EXTENSIONS默认中间件方式如上，程序执行时，日志的头部有当前任务都有哪些中间件加载，按需在对应管道中配置为 None 即可关闭
    # 同理 SPIDER_MIDDLEWARES / DOWNLOADER_MIDDLEWARES 这两个“中间件配置”字典也可以用相同的方式关掉 scrapy 默认组件
    # 【*】注意：不同分类的默认中间件需在对应分类的“中间件配置”字典中配置才能关闭，
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

MEDIA_ALLOW_REDIRECTS = True # 图片下载时默认打开该开关，一定程度上能规避一些图片下载的问题。