# -*- coding: utf-8 -*-
# 挂钩中间件加载的处理，让通过“字符串”加载中间件的函数能够同时兼容用“类”加载中间件
import scrapy.utils.misc
import scrapy.utils.deprecate
_bak_load_object      = scrapy.utils.misc.load_object
_bak_update_classpath = scrapy.utils.deprecate.update_classpath
def _load_object(path_or_class):
    try: return _bak_load_object(path_or_class)
    except: return path_or_class
def _update_classpath(path_or_class):
    try: return _bak_update_classpath(path_or_class)
    except: return path_or_class
scrapy.utils.misc.load_object = _load_object
scrapy.utils.deprecate.update_classpath = _update_classpath
# 解决各种需要重新请求的时拷贝 Request 对象没有自动包含 _plusmeta 的异常，是魔法
from scrapy import Request
def replace(self, *args, **kwargs):
    for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta',
              'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
        kwargs.setdefault(x, getattr(self, x))
    cls = kwargs.pop('cls', self.__class__)
    clz = cls(*args, **kwargs)
    clz._plusmeta = self._plusmeta
    clz._plusmeta['replace'] = True
    return clz
Request.replace = replace

# 调度器

import importlib
import six
from scrapy.utils.misc import load_object
class Scheduler(object):
    def __init__(self, server,
                 persist=False,
                 flush_on_start=False,
                 queue_key=None,
                 queue_cls=None,
                 dupefilter_key=None,
                 dupefilter_cls=None,
                 idle_before_close=0,
                 serializer=None):
        if idle_before_close < 0:
            raise TypeError("idle_before_close cannot be negative")
        self.server = server
        self.persist = persist
        self.flush_on_start = flush_on_start
        self.queue_key = queue_key or defaults.SCHEDULER_QUEUE_KEY
        self.queue_cls = queue_cls or defaults.SCHEDULER_QUEUE_CLASS
        self.dupefilter_key = dupefilter_key or defaults.SCHEDULER_DUPEFILTER_KEY
        self.dupefilter_cls = dupefilter_cls or defaults.SCHEDULER_DUPEFILTER_CLASS
        self.idle_before_close = idle_before_close
        self.serializer = serializer
        self.stats = None
    def __len__(self):
        return len(self.queue)
    @classmethod
    def from_settings(cls, settings):
        kwargs = {
            'persist': settings.getbool('SCHEDULER_PERSIST'),
            'flush_on_start': settings.getbool('SCHEDULER_FLUSH_ON_START'),
            'idle_before_close': settings.getint('SCHEDULER_IDLE_BEFORE_CLOSE'),
        }
        optional = {
            'queue_key': 'SCHEDULER_QUEUE_KEY',
            'queue_cls': 'SCHEDULER_QUEUE_CLASS',
            'dupefilter_key': 'SCHEDULER_DUPEFILTER_KEY',
            'dupefilter_cls': 'SCHEDULER_DUPEFILTER_CLASS',
            'serializer': 'SCHEDULER_SERIALIZER',
        }
        for name, setting_name in optional.items():
            val = settings.get(setting_name)
            if val:
                kwargs[name] = val
        if isinstance(kwargs.get('serializer'), six.string_types):
            kwargs['serializer'] = importlib.import_module(kwargs['serializer'])
        server = connection.from_settings(settings)
        server.ping()
        return cls(server=server, **kwargs)
    @classmethod
    def from_crawler(cls, crawler):
        instance = cls.from_settings(crawler.settings)
        instance.stats = crawler.stats
        return instance
    def open(self, spider):
        self.spider = spider
        try:
            self.queue = load_object(self.queue_cls)(
                server=self.server,
                spider=spider,
                key=self.queue_key % {'spider': spider.name},
                serializer=self.serializer,
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate queue class '%s': %s",
                             self.queue_cls, e)
        try:
            self.df = load_object(self.dupefilter_cls)(
                server=self.server,
                key=self.dupefilter_key % {'spider': spider.name},
                debug=spider.settings.getbool('DUPEFILTER_DEBUG'),
            )
        except TypeError as e:
            raise ValueError("Failed to instantiate dupefilter class '%s': %s",
                             self.dupefilter_cls, e)
        if self.flush_on_start:
            self.flush()
        if len(self.queue):
            spider.log("Resuming crawl (%d requests scheduled)" % len(self.queue))
    def close(self, reason):
        if not self.persist:
            self.flush()
    def flush(self):
        self.df.clear()
        self.queue.clear()
    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return False
        if self.stats:
            self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queue.push(request)
        return True
    def next_request(self):
        block_pop_timeout = self.idle_before_close
        request = self.queue.pop(block_pop_timeout)
        if request and self.stats:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request
    def has_pending_requests(self):
        return len(self) > 0

# 过滤器

import logging
import time
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
logger = logging.getLogger(__name__)
class RFPDupeFilter(BaseDupeFilter):
    logger = logger
    def __init__(self, server, key, debug=False):
        self.server = server
        self.key = key
        self.debug = debug
        self.logdupes = True
    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)
    def request_seen(self, request):
        tid = request._plusmeta.get('taskid')
        if tid:
            fp = self.request_fingerprint(request)
            added = self.server.sadd(self.key.format(tid), fp)
            return added == 0
    def request_fingerprint(self, request):
        return request_fingerprint(request)
    def close(self, reason=''):
        self.clear()
    def clear(self):
        self.server.delete(self.key)
    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

# 请求队列

import six
from scrapy.http import Request
from scrapy.utils.python import to_unicode, to_native_str
from scrapy.utils.misc import load_object
def request_to_dict(request, spider=None):
    def _find_method(obj, func):
        if obj:
            return func.__name__
        raise ValueError("Function %s is not a method of: %s" % (func, obj))
    cb = request.callback
    if callable(cb):
        cb = _find_method(spider, cb)
    eb = request.errback
    if callable(eb):
        eb = _find_method(spider, eb)
    if not request._plusmeta.pop('replace', None):
        request._plusmeta.update({'__callerr__':{'callback':cb,'errback':eb}})
    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': 'parse',
        'errback': eb,
        'method': request.method,
        'headers': dict(request.headers),
        'body': request.body,
        'cookies': request.cookies,
        'meta': request.meta,
        '_encoding': request._encoding,
        'priority': request.priority,
        'dont_filter': request.dont_filter,
        'flags': request.flags,
        '_plusmeta':request._plusmeta,
    }
    if type(request) is not Request:
        d['_class'] = request.__module__ + '.' + request.__class__.__name__
    return d
def request_from_dict(d, spider=None):
    def _get_method(obj, name):
        name = str(name)
        try:
            return getattr(obj, name)
        except AttributeError:
            raise ValueError("Method %r not found in: %s" % (name, obj))
    cb = d['callback']
    if cb and spider:
        cb = _get_method(spider, cb)
    eb = d['errback']
    if eb and spider:
        eb = _get_method(spider, eb)
    request_cls = load_object(d['_class']) if '_class' in d else Request
    _cls = request_cls(
        url=to_native_str(d['url']),
        callback=cb,
        errback=eb,
        method=d['method'],
        headers=d['headers'],
        body=d['body'],
        cookies=d['cookies'],
        meta=d['meta'],
        encoding=d['_encoding'],
        priority=d['priority'],
        dont_filter=d['dont_filter'],
        flags=d.get('flags'))
    _cls._plusmeta = d['_plusmeta']
    return _cls
try:
    import cPickle as pickle  # PY2
except ImportError:
    import pickle
class picklecompat:
    @staticmethod
    def loads(s):
        return pickle.loads(s)
    @staticmethod
    def dumps(obj):
        return pickle.dumps(obj, protocol=-1)
class Base(object):
    def __init__(self, server, spider, key, serializer=None):
        if serializer is None:
            serializer = picklecompat
        if not hasattr(serializer, 'loads'):
            raise TypeError("serializer does not implement 'loads' function: %r"
                            % serializer)
        if not hasattr(serializer, 'dumps'):
            raise TypeError("serializer '%s' does not implement 'dumps' function: %r"
                            % serializer)
        self.server = server
        self.spider = spider
        self.key = key % {'spider': spider.name}
        self.serializer = serializer
    def _encode_request(self, request):
        obj = request_to_dict(request, self.spider)
        return self.serializer.dumps(obj)
    def _decode_request(self, encoded_request):
        obj = self.serializer.loads(encoded_request)
        return request_from_dict(obj, self.spider)
    def __len__(self):
        raise NotImplementedError
    def push(self, request):
        raise NotImplementedError
    def pop(self, timeout=0):
        raise NotImplementedError
    def clear(self):
        self.server.delete(self.key)
class FifoQueue(Base):
    def __len__(self):
        return self.server.llen(self.key)
    def push(self, request):
        self.server.lpush(self.key, self._encode_request(request))
    def pop(self, timeout=0):
        if timeout > 0:
            data = self.server.brpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.rpop(self.key)
        if data:
            return self._decode_request(data)
class PriorityQueue(Base):
    def __len__(self):
        return self.server.zcard(self.key)
    def push(self, request):
        data = self._encode_request(request)
        score = -request.priority
        self.server.execute_command('ZADD', self.key, score, data)
    def pop(self, timeout=0):
        pipe = self.server.pipeline()
        pipe.multi()
        pipe.zrange(self.key, 0, 0).zremrangebyrank(self.key, 0, 0)
        results, count = pipe.execute()
        if results:
            return self._decode_request(results[0])
class LifoQueue(Base):
    def __len__(self):
        return self.server.llen(self.key)
    def push(self, request):
        self.server.lpush(self.key, self._encode_request(request))
    def pop(self, timeout=0):
        if timeout > 0:
            data = self.server.blpop(self.key, timeout)
            if isinstance(data, tuple):
                data = data[1]
        else:
            data = self.server.lpop(self.key)
        if data:
            return self._decode_request(data)

SpiderQueue = FifoQueue
SpiderStack = LifoQueue
SpiderPriorityQueue = PriorityQueue

# 日志处理

import sys
import redis
import pprint
import logging
from datetime import datetime, timedelta
logger = logging.getLogger(__name__)
from scrapy.statscollectors import StatsCollector

class RedisStatsCollector:
    e = ( 'finish_reason', )
    t = ( 'finish_time', 'start_time', )
    def __init__(self, crawler):
        self._spider_id_debg_format = crawler.settings.get('DEBUG_PC_FORMAT')
        self._spider_id_task_format = crawler.settings.get('TASK_ID_FORMAT')
        self._pc_mac    = crawler.settings.get('PCMAC')
        self._dump      = crawler.settings.getbool('STATS_DUMP')
        self._debug_pc  = crawler.settings.getbool('DEBUG_PC')
        self._local_max = crawler.settings.get('DEPTH_MAX_FORMAT')
        self._stats     = {}
        self.server     = connection.from_settings(crawler.settings)
        self.encoding   = self.server.connection_pool.connection_kwargs.get('encoding')
    def get_stats(self, spider=None):
        name = self._spider_id_debg_format % {'spider':spider.name}
        _stat = {}
        for key,val in self.server.hgetall(name).items():
            key,val = key.decode(self.encoding),val.decode(self.encoding)
            try:
                if key in self.e:  _stat[key] = val # 这里需要考虑从时间字符串加载时间 datetime.strptime(val,date_fmt) # finish_time, start_time
                elif key in self.t: _stat[key] = datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
                else: _stat[key] = int(val) 
            except: _stat[key] = val
        return _stat
    def set_stats(self, stats, spider=None):
        for key in stats:
            name = self._spider_id_debg_format % {'spider':spider.name}
            self.server.hset(name, key, stats[key])
    def get_value(self, key, default=None, spider=None):
        if spider:
            name = self._spider_id_debg_format % {'spider':spider.name}
            val = self.server.hget(name, key)
            if val:
                val = val.decode(self.encoding)
                if key in self.t:
                    ret = datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
                else:
                    if key not in self.e:
                        try:
                            ret = int(val)
                        except:
                            ret = str(val)
                    else:
                        ret = str(val)
                return ret
            else:
                return default
        else:
            return default
    def get_taskid(self, spider, deep=2):
        frame = sys._getframe() # 这里的处理比 inspect.stack() 要更省资源
        while deep:
            frame = frame.f_back
            deep -= 1
        v = frame.f_locals
        if 'request' in v:
            taskid = v['request']._plusmeta.get('taskid') or 0
        elif 'request' in v and 'response' in v:
            taskid = v['request']._plusmeta.get('taskid') or 0
        elif 'response' in v:
            taskid = v['response']._plusmeta.get('taskid') or 0
        else:
            taskid = 0
        return taskid
    def set_value(self, key, value, spider=None):
        sname = self._spider_id_debg_format % {'spider':spider.name}
        tname = self._spider_id_task_format.format(self.get_taskid(spider)) % {'spider':spider.name}
        if type(value) == datetime: value = str(value + timedelta(hours=8)) # 将默认utc时区转到中国，方便我使用
        if self._debug_pc: self.server.hset(sname, key, value)
        self.server.hsetnx(tname, key, value)
    def inc_value(self, key, count=1, start=0, spider=None):
        if spider:
            sname = self._spider_id_debg_format % {'spider':spider.name}
            tname = self._spider_id_task_format.format(self.get_taskid(spider)) % {'spider':spider.name}
            if self._debug_pc: self.server.hincrby(sname, key, count)
            self.server.hincrby(tname, key, count)
        else: pass
    def max_value(self, key, value, spider=None):
        def update_redis(key, value):
            sname = self._spider_id_debg_format % {'spider':spider.name}
            tname = self._spider_id_task_format.format(self.get_taskid(spider, 3)) % {'spider':spider.name}
            if self._debug_pc: self.server.hset(sname, key, value)
            self.server.hset(tname, key, value)
        localmax = self._local_max.format(self.get_taskid(spider)) % {'spider':spider.name}
        self._stats.setdefault(localmax, {})
        if key not in self._stats[localmax]:
            self._stats[localmax][key] = value
            update_redis(key, value)
        else:
            if value > self._stats[localmax][key]:
                self._stats[localmax][key] = value
                update_redis(key, value)
    def min_value(self, key, value, spider=None): pass
    def open_spider(self, spider): 
        spider.logger.info('Spider RedisStatsCollector opened. curr pcmac:{}.'.format(self._pc_mac))
    def close_spider(self, spider, reason): pass

# 魔改原始的日志

from scrapy.extensions import corestats
class RedisCoreStats(corestats.CoreStats):
    def __init__(self, stats): super(RedisCoreStats, self).__init__(stats)
    def spider_opened(self, spider): 
        spider.logger.info('Spider RedisCoreStats opened.')
    def spider_closed(self, spider, reason): pass
    def item_scraped(self, item, spider, response):
        self.stats.inc_value('item_scraped_count', spider=spider)
    def response_received(self, spider, request, response):
        self.stats.inc_value('response_received_count', spider=spider)
    def item_dropped(self, item, spider, exception, response):
        reason = exception.__class__.__name__
        self.stats.inc_value('item_dropped_count', spider=spider)
        self.stats.inc_value('item_dropped_reasons_count/%s' % reason, spider=spider)

# 蜘蛛

import redis
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spiders import Spider
from twisted.internet import task
import os
import sys
import json
import hmac
import pprint
import importlib
import traceback
from datetime import datetime, timedelta
def mk_work_home(path='.vscrapy'):
    home = os.environ.get('HOME')
    home = home if home else os.environ.get('HOMEDRIVE') + os.environ.get('HOMEPATH')
    path = os.path.join(home, path)
    if not os.path.isdir(path): os.makedirs(path)
    if path not in sys.path: sys.path.append(path)
    return path
def save_script_as_a_module_file(script):
    try:
        path = mk_work_home()
        filename = '_' + hmac.new(b'',script.encode(),'md5').hexdigest() + '.py'
        filepath = os.path.join(path, filename)
        if not os.path.isfile(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(script)
        return filename.replace('.py', '')
    except:
        traceback.print_exc()
def load_spider_from_module(name, module_name):
    module = importlib.import_module(module_name)
    for i in dir(module):
        c = getattr(module, i)
        n = getattr(c, 'name', None)
        s = getattr(c, 'start_requests', None)
        if s and n == name:
            return c
class RedisMixin(object):
    redis_key = None
    redis_batch_size = None
    redis_encoding = None
    server = None
    spider_objs = {}
    spider_tids = {}
    def start_requests(self):
        return self.next_requests()
    def setup_redis(self, crawler=None):
        if self.server is not None:
            return
        if crawler is None:
            crawler = getattr(self, 'crawler', None)
        if crawler is None:
            raise ValueError("crawler is required")
        settings = crawler.settings
        if self.redis_key is None:
            self.redis_key = settings.get(
                'REDIS_START_URLS_KEY', defaults.START_URLS_KEY,
            )
        self.redis_key = self.redis_key % {'name': self.name}
        if not self.redis_key.strip():
            raise ValueError("redis_key must not be empty")
        if self.redis_batch_size is None:
            self.redis_batch_size = settings.getint(
                'REDIS_START_URLS_BATCH_SIZE',
                settings.getint('CONCURRENT_REQUESTS'),
            )
        try:
            self.redis_batch_size = int(self.redis_batch_size)
        except (TypeError, ValueError):
            raise ValueError("redis_batch_size must be an integer")
        if self.redis_encoding is None:
            self.redis_encoding = settings.get('REDIS_ENCODING', defaults.REDIS_ENCODING)
        self.logger.info("Reading start URLs from redis key '%(redis_key)s' "
                         "(batch size: %(redis_batch_size)s, encoding: %(redis_encoding)s",
                         self.__dict__)
        self.server = connection.from_settings(crawler.settings)
        # 在后续的处理中，任务不再是在爬虫空闲的时候才进行任务的分配，而是一直都会执行（为了适配多任务）
        # 这样不会让一些任务得不到启动。因此 spider_idle 函数将不在负责执行 schedule_next_requests
        # 而只会抛出 DontCloseSpider 异常，
        # 并且新开一个 schedule_next_requests 函数轮询任务，用于获取启动任务
        # 并且新开一个 _stop_clear 函数轮询任务，用于检测函数停止任务
        crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        # 将日志的模板拿到这个对象中，后续函数需要用到
        self._clear_debug_pc   = crawler.settings.getbool('CLEAR_DEBUG_PC')
        self._clear_dupefilter = crawler.settings.getbool('CLEAR_DUPEFILTER')
        self._spider_id_debg_format = crawler.settings.get('DEBUG_PC_FORMAT')
        self._spider_id_task_format = crawler.settings.get('TASK_ID_FORMAT')
        self._spider_id_dupk_format = crawler.settings.get('SCHEDULER_DUPEFILTER_KEY')
        # 这里是将该任务开启绑定两个定时执行，永不停止的函数
        # 1/ 为了检查已经停止的任务并且清理任务的空间。
        # 2/ 为了获取到新的 start_url 开启新的任务脚本进行任务的初始化并且处理任务空间的问题。
        self.limit_check = 0 # 这个参数是想让不同的任务的检查时机稍微错开一点，不要都挤在 _stop_clear 一次迭代中
        self.limit_same  = 2 # 日志快照连续相同的次数
        self.interval    = 5 # 多少秒执行一次 检测关闭任务
        # (理论上平均检测关闭的时间大概为 (limit_check+1) * (limit_same+1) * interval )
        # 测试时可以适量调整小一些方便查看框架的问题
        self.interval_s  = 2 # 多少秒执行一次 检测启动任务
        self.limit_log   = 8 # 额外的配置，check stoping 限制显示任务数，防止出现如有几百个任务每次都要全部打印的情况。
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
    def spider_opened(self):
        task.LoopingCall(self._stop_clear).start(self.interval)
        task.LoopingCall(self.schedule_next_requests).start(self.interval_s)
    def _get_snapshot(self, stat_key):
        _snapshot = self.server.hgetall(stat_key)
        enqueue, dequeue = 0, 0
        snapshot = {}
        for k,v in _snapshot.items():
            if k.decode() == 'scheduler/enqueued/redis': enqueue += int(v.decode())
            if k.decode() == 'scheduler/dequeued/redis': dequeue += int(v.decode())
            snapshot[k.decode()] = v.decode()
        return snapshot, enqueue, dequeue
    def _stop_clear(self):
        taskids = []
        spider_tids_shot = self.spider_tids.copy()
        for taskid in spider_tids_shot:
            taskids.append(taskid)
            # 在一定时间后对统计信息的快照进行处理，如果快照相同，则计数
            # 相似数超过N次，则代表任务已经收集不到数据了，遂停止任务，并写入任务停止时间，（设置的时间越长越准，十分钟内差不多了）
            if self.spider_tids[taskid]['check_times'] != self.limit_check:
                self.spider_tids[taskid]['check_times'] += 1
            else:
                self.spider_tids[taskid]['check_times'] = 0
                stat_key = self._spider_id_task_format.format(taskid) % {'spider': self.name}

                snapshot, enqueue, dequeue = self._get_snapshot(stat_key)
                snapshot_e2d = enqueue == dequeue
                snapshot_md5 = hmac.new(b'',str(snapshot).encode(),'md5').hexdigest()
                if snapshot_md5 != self.spider_tids[taskid]['stat_snapshot'] or not snapshot_e2d:
                    self.spider_tids[taskid]['stat_snapshot'] = snapshot_md5
                    self.spider_tids[taskid]['same_snapshot_times'] = 0
                else:
                    self.spider_tids[taskid]['same_snapshot_times'] += 1
                    if self.spider_tids[taskid]['same_snapshot_times'] >= self.limit_same:
                        # 这里主要就是直接对任务结束进行收尾处理
                        # 后续需要各种删除 redis 中各种不需要的 key 来清理空间
                        # 另外再清理程序启动时生成的检测停止标签
                        if self._clear_debug_pc:
                            stat_pckey = self._spider_id_debg_format % {'spider': self.name}
                            self.server.delete(stat_pckey)
                        if self._clear_dupefilter:
                            dupefilter = self._spider_id_dupk_format.format(taskid) % {'spider': self.name}
                            self.server.delete(dupefilter)
                        module_name = self.spider_tids[taskid]['module_name']
                        # 在 redis 里面必须常驻的就是任务脚本
                        # 因为任务脚本会经过 hash 处理，以名字的 hash 作为 redis 的 key 进行存储
                        # 这样一个好处就是即便是存在大量重复的任务也只会存放一个任务脚本
                        # 同时 spider 对象也用的是脚本的 hash 作为 key 存放在执行程序的一个字典里面
                        # 为了考虑重复任务的可能，在任务结束时，删除[可能别的任务也在用的]对象的风险和开发难度很大，
                        # 实际上这种对象资源的消耗本身也比较小，所以对象也考虑常驻内存，
                        # 并且程序重启后，如果没有遇到需要用到之前任务的脚本也不会主动去实例化。节省开支。
                        # 另外还有一种恶性情况，就是还没有检查到任务停止的时候程序就意外关闭了
                        # 可能的影响：没有清理过滤池、没有写入finish_time、少数几条正在执行的任务丢失，
                        # 对其他正在执行的任务影响基本没有。所以不考虑了。
                        del self.spider_tids[taskid]
                        self.log_stat(taskid, 'finish_time')
                        snapshot,_,_ = self._get_snapshot(stat_key)
                        self.logger.info('Task {} is Stoped.\n'.format(taskid) + pprint.pformat(snapshot))
                        taskids.remove(taskid)
        if len(taskids) == 0:
            self.logger.info("Spider Task is Empty.")
        else:
            if len(taskids) > self.limit_log:
                fmt_log = '{}'.format(taskids[:self.limit_log]).replace(']',', ...][num:{}]'.format(len(taskids)))
            else:
                fmt_log = '{}'.format(taskids)
            self.logger.info("Check Task Stoping {}.".format(fmt_log))
    def schedule_next_requests(self):
        for req in self.next_requests():
            self.crawler.engine.crawl(req, spider=self)
    # 下面的部分主要是处理 start_url 的部分，这里的处理是永久打开直至程序关闭的
    # 原本 scrapy-redis 是用这个来接收一个起始 url 字符串，不过现在改成了接收一个json数据传递脚本数据
    # 将此处魔改成对传递过来的参数各种初始化的地方，在发送端生成id后传入这边进行处理
    # 这里可以传过来一个简单的 json 数据来装脚本的代码部分，方便脚本的传递以及实例化
    def next_requests(self):
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        fetch_one = self.server.spop if use_set else self.server.lpop
        found = 0
        while found < self.redis_batch_size:
            data = fetch_one(self.redis_key)
            if not data:
                break
            data = json.loads(data)
            # 这里需要生成最初的请求,基本上就是需要通过传过来的data进行最初的脚本运行
            # 通过生成对象来调配该对象的 start_requests 函数来生成最开始的请求
            # 需要传递的最初的json结构需要包含三个关键字参数
            # 1/ 'taskid'  # 任务id # 这个由任务发送端自动生成。
            # 2/ 'name'    # 爬虫的名字
            # 3/ 'script'  # 脚本字符串
            # 这里暂时还没有处理异常情况，是因为异常信息的处理这时还没有决定
            # 不过比较符合心理预期的很可能是挂钩所有日志一并传入带 taskid 分配处理的管道
            module_name = save_script_as_a_module_file(data['script'])
            spider_obj  = load_spider_from_module(data['name'], module_name)
            taskid      = None
            for i in spider_obj().start_requests():
                if taskid is None: # 确认执行任务后再写入script到redis，防止浪费redis中的脚本存放空间
                    taskid = data['taskid']
                    self.server.set('vscrapy:script:{}'.format(module_name), json.dumps(data))
                    self.log_stat(taskid, 'start_time')
                    self.spider_tids[taskid] = {
                        'check_times': 0, 
                        'stat_snapshot': None, 
                        'same_snapshot_times': 0,
                        'module_name': module_name
                    }
                # 这里的重点就是 _plusmeta 的内容一定要是可以被序列化的数据，否则任务无法启动
                # 所以后续的开发这里需要注意，因为后续可能会增加其他的参数进去
                _plusmeta = data.copy()
                _plusmeta.pop('taskid', None)
                _plusmeta.pop('module_name', None)
                _plusmeta.pop('spider_name', None)
                _plusmeta.pop('script', None)
                _plusmeta.pop('name', None)
                i._plusmeta = _plusmeta
                i._plusmeta.update({
                    'taskid': taskid, 
                    'module_name': module_name, 
                    'spider_name': data['name'],
                })
                yield i
                found += 1
            break
        if found:
            self.logger.debug("Read %s requests(start_requests) from new task %s.", found, taskid)
    def log_stat(self, taskid, key):
        # 由于默认的任务开启和关闭日志不是真实的任务开关闭时间
        # 所以这里需要使用自己设定的任务开启和关闭的的时间来处理任务状态
        tname = self._spider_id_task_format.format(taskid) % {'spider': self.name}
        value = str(datetime.utcnow() + timedelta(hours=8)) # 使用中国时区，方便我自己使用
        self.server.hsetnx(tname, key, value)
    def spider_idle(self):
        raise DontCloseSpider
class RedisSpider(RedisMixin, Spider):
    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        obj = super(RedisSpider, self).from_crawler(crawler, *args, **kwargs)
        obj.setup_redis(crawler)
        return obj

# 默认配置

import redis
import uuid
class defaults:
    REDIS_CLS = redis.StrictRedis
    REDIS_ENCODING    = 'utf-8'
    REDIS_PARAMS = {
        'socket_timeout': 30,
        'socket_connect_timeout': 30,
        'retry_on_timeout': True,
        'encoding': REDIS_ENCODING,
    }
    PCMAC, SNAPSHOTID           = uuid.UUID(int=uuid.getnode()).hex[-12:], str(uuid.uuid4())[:5]
    SCHEDULER_QUEUE_CLASS       = PriorityQueue
    SCHEDULER_DUPEFILTER_CLASS  = RFPDupeFilter
    SCHEDULER                   = Scheduler
    STATS_CLASS                 = RedisStatsCollector
    PIPELINE_KEY                = 'vscrapy:gqueue:%(spider)s:items'
    SCHEDULER_QUEUE_KEY         = 'vscrapy:gqueue:%(spider)s/requests'
    SCHEDULER_DUPEFILTER_KEY    = 'vscrapy:gqueue:%(spider)s/taskid/{}/dupefilter'
    START_URLS_KEY              = 'vscrapy:gqueue:%(name)s:start_urls'
    DUPEFILTER_KEY              = 'dupefilter:%(timestamp)s'
    DEBUG_PC_FORMAT             = 'vscrapy:stats:pc/{}:rdkey/{}/stat/%(spider)s'.format(PCMAC, SNAPSHOTID)
    TASK_ID_FORMAT              = 'vscrapy:stats:%(spider)s/taskid/{}/stat'
    DEPTH_MAX_FORMAT            = 'taskid:{}:%(spider)s'
    REDIS_ITEMS_KEY             = 'vscrapy:gqueue:%(spider)s/taskid/{}/items'
    CLEAR_DUPEFILTER            = True
    START_URLS_AS_SET           = False
    CLEAR_DEBUG_PC              = False
    DEBUG_PC                    = False
    LOG_LEVEL                   = 'DEBUG'
import six
from scrapy.utils.misc import load_object
SETTINGS_PARAMS_MAP = {
    'REDIS_URL': 'url',
    'REDIS_HOST': 'host',
    'REDIS_PORT': 'port',
    'REDIS_ENCODING': 'encoding',
}
class connection:
    @staticmethod
    def get_redis_from_settings(settings):
        params = defaults.REDIS_PARAMS.copy()
        params.update(settings.getdict('REDIS_PARAMS'))
        for source, dest in SETTINGS_PARAMS_MAP.items():
            val = settings.get(source)
            if val:
                params[dest] = val
        if isinstance(params.get('redis_cls'), six.string_types):
            params['redis_cls'] = load_object(params['redis_cls'])
        return connection.get_redis(**params)
    from_settings = get_redis_from_settings
    @staticmethod
    def get_redis(**kwargs):
        redis_cls = kwargs.pop('redis_cls', defaults.REDIS_CLS)
        url = kwargs.pop('url', None)
        if url:
            return redis_cls.from_url(url, **kwargs)
        else:
            return redis_cls(**kwargs)

# 蜘蛛中间件需要暂时无用，后续考虑扩展代理相关处理

class VSpiderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_spider_input(self, response, spider):
        return None
    def process_spider_output(self, response, result, spider):
        for i in result:
            yield i
    def process_spider_exception(self, response, exception, spider):
        pass
    def process_start_requests(self, start_requests, spider):
        for r in start_requests:
            yield r
    def spider_opened(self, spider):
        spider.logger.info('Spider VSpiderMiddleware opened.')

# 下载中间件需要将 process_response 函数内挂钩一个微小的部分解决一个分布式异常

class VDownloaderMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    def process_request(self, request, spider):
        return None
    def process_response(self, request, response, spider):
        response._plusmeta = request._plusmeta
        return response
    def process_exception(self, request, exception, spider):
        pass
    def spider_opened(self, spider):
        spider.logger.info('Spider VDownloaderMiddleware opened.')

# item中间件尾部，依据在item中是否存在 _b2b89079b2f7befcf4691a98a3f0a2a2 字段来决定数据是否存放入 redis

from scrapy.utils.misc import load_object
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
default_serialize = ScrapyJSONEncoder().encode
class RedisPipeline_END(object):
    def __init__(self, server,
                 key=defaults.PIPELINE_KEY,
                 serialize_func=default_serialize):
        self.server = server
        self.key = key
        self.serialize = serialize_func
    @classmethod
    def from_settings(cls, settings):
        params = {
            'server': connection.from_settings(settings),
        }
        if settings.get('REDIS_ITEMS_KEY'):
            params['key'] = settings['REDIS_ITEMS_KEY']
        if settings.get('REDIS_ITEMS_SERIALIZER'):
            params['serialize_func'] = load_object(
                settings['REDIS_ITEMS_SERIALIZER']
            )
        return cls(**params)
    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)
    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)
    def _process_item(self, item, spider):
        if item:
            _item = item.copy()
            if _item.pop('_b2b89079b2f7befcf4691a98a3f0a2a2', None):
                key = self.item_key(item, spider)
                data = self.serialize(_item)
                self.server.lpush(key, data)
                return item
    def item_key(self, item, spider):
        return self.key.format(item.get('_b2b89079b2f7befcf4691a98a3f0a2a2').get('taskid')) % {'spider': spider.name}

# 基础 item 中间件模板
class VPipeline(object):
    def process_item(self, item, spider):
        print('------------------------------ split ------------------------------')
        if item.get('_b2b89079b2f7befcf4691a98a3f0a2a2'):
            # 这里可以接收到提交任务时候传递的参数，根据需要的参数进行针对性的保存处理
            # 例如不同任务指定不同的存储表名字
            _plusmeta = item.get('_b2b89079b2f7befcf4691a98a3f0a2a2').get('_plusmeta')
            print('_plusmeta:', _plusmeta)
        import pprint
        pprint.pprint(item)
        return item

# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from lxml import etree

def lineReceived(self, line):
    if line[-1:] == b'\r': line = line[:-1]
    if self.state == u'STATUS': self.statusReceived(line); self.state = u'HEADER'
    elif self.state == u'HEADER':
        if not line or line[0] not in b' \t':
            if self._partialHeader is not None:
                _temp = b''.join(self._partialHeader).split(b':', 1)
                name, value = _temp if len(_temp) == 2 else (_temp[0], b'')
                self.headerReceived(name, value.strip())
            if not line: self.allHeadersReceived()
            else: self._partialHeader = [line]
        else: self._partialHeader.append(line)
import twisted.web._newclient
twisted.web._newclient.HTTPParser.lineReceived = lineReceived
# 以下补丁代码：解决 idna 库过于严格，导致带有下划线的 hostname 无法验证通过的异常
import idna.core
_check_label_bak = idna.core.check_label
def check_label(label):
    try: return _check_label_bak(label)
    except idna.core.InvalidCodepoint: pass
idna.core.check_label = check_label

import json
import types
import traceback
from scrapy import Request

class VSpider(RedisSpider):
    name = 'v'
    def parse(self, response):
        _plusmeta   = response._plusmeta.copy()
        taskid      = _plusmeta.pop('taskid')
        spider_name = _plusmeta.pop('spider_name')
        module_name = _plusmeta.pop('module_name')
        __callerr__ = _plusmeta.pop('__callerr__')

        # 在传递脚本的 start_requests 执行时会执行一次将脚本加载成对象放入
        # 如果是非 start_requests 执行的任务则需要在 parse 函数里面确认加载进框架
        # 并且不同的机器也需要考虑脚本的分配获取，所以脚本也需要上传。
        if module_name not in self.spider_objs:
            try:
                self.spider_objs[module_name] = load_spider_from_module(spider_name, module_name)
            except:
                data = self.server.get('vscrapy:script:{}'.format(module_name))
                data = json.loads(data)
                module_name = save_script_as_a_module_file(data['script'])
                self.spider_objs[module_name] = load_spider_from_module(spider_name, module_name)

        spider = self.spider_objs[module_name]
        parsefunc = getattr(spider, __callerr__.get('callback'))
        parsedata = parsefunc(spider, response)
        if parsedata:
            if getattr(parsedata, '__iter__') and isinstance(parsedata, (list, types.GeneratorType)):
                for r in parsedata:
                    if isinstance(r, (Request,)):
                        r._plusmeta = response._plusmeta
                        yield r
                    else:
                        yield self._parse_item(r, taskid, _plusmeta) # 这里是数据
            elif isinstance(parsedata, (Request,)):
                r = parsedata
                r._plusmeta = response._plusmeta
                yield r
            else:
                yield self._parse_item(parsedata, taskid, _plusmeta) # 这里是数据

    def _parse_item(self, item, taskid, _plusmeta):
        # item中间件尾部，依据在item中是否存在 _b2b89079b2f7befcf4691a98a3f0a2a2 字段来决定数据是否存放入 redis
        # 如果在“item管道”尾部item存在该字段则自动抛弃该字段并写入 gqueue 管道
        if item:
            try:
                ret = dict(item)
                ret['_b2b89079b2f7befcf4691a98a3f0a2a2'] = {}
                ret['_b2b89079b2f7befcf4691a98a3f0a2a2']['taskid'] = taskid
                ret['_b2b89079b2f7befcf4691a98a3f0a2a2']['spider'] = self.name
                ret['_b2b89079b2f7befcf4691a98a3f0a2a2']['_plusmeta'] = _plusmeta
                return ret
            except:
                return TypeError(traceback.format_exc())

if __name__ == '__main__':
    import time
    from scrapy.crawler import CrawlerProcess
    timestamp = time.strftime("%Y%m%d_%H%M%S", time.localtime()) # 年月日_时分秒
    filename = 'v{}.json'.format(timestamp) # 这是输出文件名字（解开 'FEED_URI' 配置注释生效）

    p = CrawlerProcess({
        'MEDIA_ALLOW_REDIRECTS':    True,         # 允许图片下载地址重定向，存在图片下载需求时，请尽量使用该设置
        # 'DOWNLOAD_TIMEOUT':         8,          # 全局请求超时，默认180。也可以在 meta 中配置单个请求的超时( download_timeout )
        # 'DOWNLOAD_DELAY':           1,          # 全局下载延迟，这个配置相较于其他的节流配置要直观很多

        'ITEM_PIPELINES': {
            VPipeline:              101,        # 基础中间件模板，使用这个自定义怎么处理收集到的数据
            RedisPipeline_END:      999,        # 默认尾部中间件，如果没有前面没有处理，则自动将数据存储到 redis
        },
        'SPIDER_MIDDLEWARES': {
            VSpiderMiddleware:      0,
        },
        'DOWNLOADER_MIDDLEWARES': {
            VDownloaderMiddleware:  0, 
        },
        'EXTENSIONS': {
            'scrapy.extensions.telnet.TelnetConsole': None, # 关闭这个插件，我不用
            'scrapy.extensions.memusage.MemoryUsage': None, # 同样的理由，我不用
            'scrapy.extensions.logstats.LogStats':    None, # 关闭这个日志输出，因为无法获取当前任务id，遂放弃
            'scrapy.extensions.corestats.CoreStats':  None, # 关闭这个日志处理，使用魔改的日志处理
            RedisCoreStats: True,
        },
        'SCHEDULER':                    defaults.SCHEDULER,
        'STATS_CLASS':                  defaults.STATS_CLASS,
        'PIPELINE_KEY':                 defaults.PIPELINE_KEY,
        'SCHEDULER_QUEUE_KEY':          defaults.SCHEDULER_QUEUE_KEY,
        'SCHEDULER_DUPEFILTER_KEY':     defaults.SCHEDULER_DUPEFILTER_KEY,
        'START_URLS_KEY':               defaults.START_URLS_KEY,
        'DUPEFILTER_KEY':               defaults.DUPEFILTER_KEY,
        'DEBUG_PC_FORMAT':              defaults.DEBUG_PC_FORMAT,
        'TASK_ID_FORMAT':               defaults.TASK_ID_FORMAT,
        'DEPTH_MAX_FORMAT':             defaults.DEPTH_MAX_FORMAT,
        'REDIS_ITEMS_KEY':              defaults.REDIS_ITEMS_KEY,                    
        'LOG_LEVEL':                    defaults.LOG_LEVEL,               # 默认:DEBUG   # 日志等级
        'CLEAR_DUPEFILTER':             defaults.CLEAR_DUPEFILTER,        # 默认:True    # 任务结束是否删除过滤池
        'START_URLS_AS_SET':            defaults.START_URLS_AS_SET,       # 默认:False
        'CLEAR_DEBUG_PC':               defaults.CLEAR_DEBUG_PC,          # 默认:False   # 任务结束时清理pc调试日志
        'DEBUG_PC':                     defaults.DEBUG_PC,                # 默认:False   # 是否使用pc调试
        'PCMAC':                        defaults.PCMAC,                   # 本机mac      # 方便分布式调试某台机器
        'REDIS_PARAMS':{
            'host':     'localhost',    # redis 链接配置
            'port':     6379,           # redis 链接配置
            'password': None,           # redis 链接配置
            'db':       0,              # redis 链接配置
        }
    })
    p.crawl(VSpider)
    p.start()

# 以上代码为服务器爬虫代码，
# 1 配置好你需要用的redis服务器，
# 2 配置好以上代码中的 redis 链接配置(REDIS_PARAMS)
# 3 将上面的脚本保存到某个脚本中，直接执行脚本，服务即处于挂起状态等待你提交任务





# 以下代码为客户端爬虫代码
# 1 配置好下面代码中的redis 链接配置(REDIS_PARAMS)
# 2 使用时将以下代码放至 spider 脚本顶部即可，按照正常启动爬虫的方式启动
#   爬虫则自动将本地的爬虫脚本代码发送至分布式，等待执行
import re
import redis
import inspect
from scrapy.crawler import CrawlerProcess
def start(self, stop_after_crawl=True):
    REDIS_PARAMS = {
        'host':     'localhost',
        'port':     6379,
        'password': None,
        'db':       0,
    }
    def _send_script_start_work(spider_name, script, server):
        taskid = server.incrby('vscrapy:taskidx')
        jsondata = { 
            'taskid': taskid, 
            'name': spider_name,
            'script': script, 
            'mykey': 'testkey', # jsondata 里还可以传递自己想传递的参数，在分布式的 item管道中可以获取该参数，自定义后续处理方式
        }
        server.lpush('vscrapy:gqueue:v:start_urls', json.dumps(jsondata))
        return jsondata
    server = redis.StrictRedis(**REDIS_PARAMS)
    spider_name = VSpider.name
    spider_script = inspect.getsource(VSpider)
    with open(__file__, encoding='utf-8') as f:
        script = re.sub('.*?CrawlerProcess.start *= *start', '', f.read(), flags=re.S).strip()
        assert spider_script in script, '可能存在编码不一样的问题，请将该代码处理成 utf-8格式。'
        script = script.split(spider_script)[0] + spider_script
    jsondata = _send_script_start_work(spider_name, script, server)
    jsondata.pop('script')
    print('send task:')
    print(json.dumps(jsondata,indent=4))
CrawlerProcess.start = start