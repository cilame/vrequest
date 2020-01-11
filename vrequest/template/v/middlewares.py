# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class VSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class VDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)






# 配置 selenium 的使用方式
import time
from scrapy.http import HtmlResponse
class VSeleniumMiddleware(object):
    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s
    def process_request(self, request, spider):
        try:
            self.webdriver.get(url=request.url)
            time.sleep(2)
            # 部分智能等待的代码，提高浏览器效率的处理
            # from selenium.webdriver.common.by import By
            # from selenium.webdriver.support import expected_conditions as EC
            # from selenium.webdriver.support.wait import WebDriverWait as wbw
            # locator = (By.XPATH, '//img[@class="focus-item-img"]')
            # # wbw(self.webdriver,10).until(EC.presence_of_element_located(locator)) # 判断某个元素是否被加到了dom树里
            # wbw(self.webdriver,10).until(EC.visibility_of_element_located(locator)) # 判断某个元素是否被添加到了dom里并且可见，即宽和高都大于0
            current_url = self.webdriver.current_url
            page_source = self.webdriver.page_source
        except Exception as e:
            return self._parse_selenium_temp_exceptions(request, spider, e)
        # 若是出现请求异常(验证码，或者重新登陆之类的处理)，请在这里判断 page_source 是否是异常情况，并在这里处理重新进行登录或其他
        h = HtmlResponse(
            url      = current_url,
            headers  = {'Selenium':'Selenium cannot get a certain headers, This is the information created automatically by middleware.'},
            body     = page_source,
            encoding = 'utf-8',
            request  = request
        )
        return h
    def process_response(self, request, response, spider):
        return response
    def spider_opened(self, spider):
        spider.logger.info('Spider %s opened: %s' % (self.__class__.__name__, spider.name))
        self._open_webdriver()
        self._login()
    def spider_closed(self):
        if getattr(self, 'webdriver', None): self.webdriver.quit()
    def _parse_selenium_temp_exceptions(self, request, spider, e):
        stats = spider.crawler.stats
        if 'Failed to establish a new connection' in str(e): # 仅仅捕捉浏览器异常关闭的异常，尝试重启，并重新将请求发送到队列
            if getattr(self, 'restart_show_toggle', None) is None:
                self.restart_show_toggle = True
            if self.restart_show_toggle:
                self.restart_show_toggle = False # 让 Catch webdriver 仅显示一次
                spider.logger.info('Catch webdriver exception:{}, try to restart webdriver.'.format(e.__class__))
            self._open_webdriver()
            retries = request.meta.get('selenium_retry_times', 0) + 1 # 在 selenium 异常无法重启处理情况下一个请求最多尝试共3次请求
            if retries <= 3:
                retryreq = request.copy()
                retryreq.meta['selenium_retry_times'] = retries
                retryreq.dont_filter = True
                stats.inc_value('selenium_retry/count')
                return retryreq
            else:
                stats.inc_value('selenium_retry/max_reached')
                spider.logger.info("Gave up selenium_retrying %(request)s (failed %(retries)d times)",
                            {'request': request, 'retries': retries})
        else:
            stats.inc_value('selenium_unknow_error/count')
            stats.inc_value('selenium_unknow_error/reason_count/%s' % e.__class__.__name__)
            import traceback
            spider.logger.info('\n'+traceback.format_exc().strip())
    def _open_webdriver(self): # 该函数同时作为重启 webdriver 功能使用
        try: self.spider_closed()
        except: pass
        from selenium import webdriver
        option = webdriver.ChromeOptions()
        extset = ['enable-automation', 'ignore-certificate-errors']
        ignimg = "profile.managed_default_content_settings.images"
        mobile = {'deviceName':'Galaxy S5'}
        option.add_argument("--disable-infobars")                       # 旧版本关闭“chrome正受到自动测试软件的控制”信息
        option.add_experimental_option("excludeSwitches", extset)       # 新版本关闭“chrome正受到自动测试软件的控制”信息
        option.add_experimental_option("useAutomationExtension", False) # 新版本关闭“请停用以开发者模式运行的扩展程序”信息
        # option.add_experimental_option('mobileEmulation', mobile)     # 是否使用手机模式打开浏览器
        # option.add_experimental_option("prefs", {ignore_image: 2})    # 开启浏览器时不加载图片(headless模式该配置无效)
        # option.add_argument('--start-maximized')                      # 开启浏览器时是否最大化(headless模式该配置无效)
        # option.add_argument('--headless')                             # 无界面打开浏览器
        # option.add_argument('--window-size=1920,1080')                # 无界面打开浏览器时候只能用这种方式实现最大化
        # option.add_argument('--disable-gpu')                          # 禁用 gpu 硬件加速
        # option.add_argument("--auto-open-devtools-for-tabs")          # 开启浏览器时候是否打开开发者工具(F12)
        # option.add_argument("--user-agent=Mozilla/5.0 HELL")          # 修改 UA 信息
        # option.add_argument('--proxy-server=http://127.0.0.1:8888')   # 增加代理
        self.webdriver = webdriver.Chrome(chrome_options=option)
    def _login(self):
        # 如果有登录处理，则写在这里
        pass