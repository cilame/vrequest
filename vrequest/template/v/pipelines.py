# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
from scrapy import Request, Selector
from lxml import etree
import re
import json
from urllib.parse import unquote, quote

# 基础 item 中间件模板
class VPipeline(object):
    def process_item(self, item, spider):
        print('\n==== 这里是动态增加的“下载中间件”部分 ====\n')
        return item

# 图片下载 item 中间件
import logging, hashlib
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
class VImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield Request(item['src'], meta=item) 
    def file_path(self, request, response=None, info=None):
        url = request if not isinstance(request, Request) else request.url
        image_name = request.meta.get('image_name') # 使用 item中的 image_name 字段作为文件名进行存储，没有该字段则使用 url的 md5作为文件名存储
        image_name = re.sub(r'[/\\:\*"<>\|\?]', '_', image_name).strip()[:80] if image_name else hashlib.md5(url.encode()).hexdigest()
        return '%s.jpg' % image_name # 生成的图片文件名字，此处可用/符号增加多级分类路径（路径不存在则自动创建），使用 image_name 请注意重名可能性。
    def item_completed(self, results, item, info): # 判断下载是否成功
        k, v = results[0]
        if not k: logging.info('download fail {}'.format(item))
        else:     logging.info('download success {}'.format(item))
        item['image_download_stat'] = 'success' if k else 'fail'
        item['image_path'] = v['path'] if k else None # 保留文件名地址
        return item

# 视频下载 item 中间件
class VVideoPipeline(object):
    def process_item(self, item, spider):
        url = item['src']
        ### 【you-get】
        import you_get.common
        you_get.common.skip_existing_file_size_check = True # 防止发现重复视频时会强制要求输入“是否覆盖”，卡住程序，默认不覆盖
        you_get.common.any_download(url, output_dir='./video', merge=True, info_only=False)
        ### 【youtube-dl】
        # from youtube_dl import YoutubeDL
        # ytdl = YoutubeDL({'outtmpl': './video/%(title)s.%(ext)s', 'ffmpeg_location':None}) # 如果已配置ffmpeg环境则不用修改
        # info = ytdl.extract_info(url, download=True)
        return item

# 数据库上传 item 中间件(不考虑字段类型处理，每个字段统统使用 MEDIUMTEXT 类型存储 json.dumps 后的 value)
# 如果有数据库字段类型的个性化处理，请非常注意的修改 insert_item 和 init_database 两个函数中对于字段类型的初始化、插入的处理，process_item无需修改。
import hmac, logging, traceback
from twisted.enterprise import adbapi
class VMySQLPipeline(object):
    dbn = {}
    def process_item(self, item, spider):
        mysql_config = item.pop('__mysql__', None) # 存储时自动删除配置
        if mysql_config and item:
            if type(mysql_config) is dict:
                table = mysql_config.pop('table', None)
                db = mysql_config.get('db', None) or 'vrequest'
                mysql_config.setdefault('charset','utf8mb4')
                mysql_config.setdefault('db', db)
                dbk = hmac.new(b'',json.dumps(mysql_config, sort_keys=True).encode(),'md5').hexdigest()
                if dbk not in self.dbn:
                    self.dbn[dbk] = adbapi.ConnectionPool('pymysql', **mysql_config)
                    self.init_database(self.dbn[dbk], mysql_config, db, table, item)
                self.dbn[dbk].runInteraction(self.insert_item, db, table, item)
                return item
            else:
                raise TypeError('Unable Parse mysql_config type:{}'.format(type(mysql_config)))
        else:
            return item
    def insert_item(self, conn, db, table, item):
        table_sql = ''.join(["'{}',".format(json.dumps(v, ensure_ascii=False).replace("'","\\'")) for k,v in item.items()])
        insert_sql = 'INSERT INTO `{}`.`{}` VALUES({})'.format(db, table, table_sql.strip(','))
        try: 
            conn.execute(insert_sql)
            logging.info('insert sql success')
        except Exception as e: 
            logging.info('insert sql fail: {}'.format(insert_sql))
            logging.error(traceback.format_exc())
    def init_database(self, pool, mysql_config, db, table, item):
        # 需要注意的是，在一些非常老的版本的mysql 里面并不支持 utf8mb4。这是 mysql 的设计缺陷，赶紧使用大于 5.5 版本的 mysql !
        # 创建db，创建表名，所有字段都以 MEDIUMTEXT 存储，用 json.dumps 保证了数据类型也能存储，后续取出时只需要每个值 json.loads 这样就能获取数据类型
        # 例如一个数字类型    123 -> json.dumps -> '123' -> json.loads -> 123，统一类型存储，取出时又能保证数据类型，这种处理会很方便
        # MEDIUMTEXT 最大能使用16M 的长度，所以对于一般的 html 文本也非常足够。如有自定义字段类型的需求，请注意修改该处。
        db, charset = mysql_config.pop('db'), mysql_config.get('charset')
        try:
            conn = pool.dbapi.connect(**mysql_config)
            cursor = conn.cursor()
            table_sql = ''.join(['`{}` MEDIUMTEXT NULL,'.format(str(k)) for k,v in item.items()])
            cursor.execute('Create Database If Not Exists {} Character Set {}'.format(db, charset))
            cursor.execute('Create Table If Not Exists `{}`.`{}` ({})'.format(db, table, table_sql.strip(',')))
            conn.commit(); cursor.close(); conn.close()
        except Exception as e:
            traceback.print_exc()

# 阿里 Oss 文件上传中间件模板
# 依赖 pip install oss2
class VOssPipeline:
    BUCKET_STORE = None
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        import oss2
        aid = 'kkkkkkkkkkkkkkkkkkkkkkkk'
        ack = 'vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv'
        enp = 'http://oss-cn-hangzhou.aliyuncs.com'
        _bucket = '<bucket name>'
        VOssPipeline.BUCKET_STORE = oss2.Bucket(oss2.Auth(aid,ack), enp, _bucket)
        return s
    def process_item(self, item, spider):
        # 示例: 用于将下载到的图片上传到Oss的代码如下
        # ipath = item.get('image_path')
        # if ipath and os.path.isfile(ipath): self.update_data(ipath, ipath)
        return item
    def update_data(self, object_name, localfile_name):
        VOssPipeline.BUCKET_STORE.put_object_from_file(object_name, localfile_name)