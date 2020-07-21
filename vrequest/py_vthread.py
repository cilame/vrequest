class pool:
    import time,queue,traceback,builtins,functools
    from threading import Thread,RLock,current_thread,main_thread
    orig_func = {}
    _org_print = print
    lock = RLock()
    class KillThreadParams(Exception): pass
    _monitor = None
    _monitor_run_num = {}
    _pool_queue = {}
    _pool_func_num = {}
    def __init__(self,pool_num=None,gqueue='v',monitor=True):
        if gqueue not in self._pool_queue:
            self._pool_queue[gqueue] = pool.queue.Queue()
        self._pool = self._pool_queue[gqueue]
        pool._patch_print()
        if monitor: self.main_monitor()
        if gqueue not in self._monitor_run_num:
            self._monitor_run_num[gqueue] = pool.queue.Queue()
        num = self._auto_pool_num(pool_num)
        if gqueue not in self._pool_func_num:
            self._pool_func_num[gqueue] = num
            self._run(num,gqueue)
        else:
            if pool_num is not None:
                self.change_thread_num(num,gqueue)
    def __call__(self,func):
        pool.orig_func[func.__name__] = func
        @pool.functools.wraps(func)
        def _run_threads(*args,**kw): self._pool.put((func,args,kw))
        return _run_threads
    @classmethod
    def change_thread_num(self,num,gqueue='v'):
        if gqueue in self._pool_func_num:
            x = self._pool_func_num[gqueue] - num
            if x < 0: self._run(abs(x),gqueue)
            if x > 0: [self._pool_queue[gqueue].put(self.KillThreadParams) for _ in range(abs(x))]
            self._pool_func_num[gqueue] = num
    @classmethod
    def main_monitor(self):
        def _func():
            while True:
                pool.time.sleep(.25)
                if not pool.main_thread().isAlive() and all(map(lambda i:i.empty(),self._monitor_run_num.values())):
                    self.close_all()
                    break
        if not self._monitor:
            self._monitor = pool.Thread(target=_func,name="MainMonitor")
            self._monitor.start()
    @classmethod
    def close_by_gqueue(self,gqueue='v'): self.change_thread_num(0,gqueue)
    @classmethod
    def close_all(self):
        for i in self._pool_func_num: self.change_thread_num(0,i)
    @classmethod
    def wait(self, gqueue='v'):
        while self.check_stop(gqueue): pool.time.sleep(.25)
    @classmethod
    def check_stop(self, gqueue='v'):
        return self._monitor_run_num[gqueue].qsize() or self._pool_queue[gqueue].qsize()
    @staticmethod
    def atom(func):
        def _atom(*arg,**kw):
            with pool.lock: return func(*arg,**kw)
        return _atom
    @staticmethod
    def _patch_print(): pool.builtins.print = pool._new_print
    @staticmethod
    def _new_print(*arg,**kw):
        with pool.lock: pool._org_print("[{}]".format(pool.current_thread().getName().center(13)),*arg,**kw)
    @staticmethod
    def _auto_pool_num(num):
        if not num:
            try:
                from multiprocessing import cpu_count
                num = cpu_count()
            except:
                print("cpu_count error. use default num 4.")
                num = 4
        return num
    @classmethod
    def _run(self,num,gqueue):
        def _pools_pull():
            ct = pool.current_thread()
            ct.setName("{}_{}".format(ct.getName(), gqueue))
            while True:
                v = self._pool_queue[gqueue].get()
                if v == self.KillThreadParams: return
                try:
                    func,args,kw = v
                    self._monitor_run_num[gqueue].put('V')
                    func(*args,**kw)
                except BaseException as e:
                    print(pool.traceback.format_exc())
                finally:
                    self._monitor_run_num[gqueue].get('V')
        for _ in range(num): pool.Thread(target=_pools_pull).start()
if __name__ == '__main__':
    # 简化代码版本的 vthread 库（分组线程池装饰器），一行代码即可实现线程池操作
    # 以下为使用/测试 “装饰器线程池” 的代码，你可以在正式使用前熟悉一下使用方法
    import time, random
    # 被 pool 装饰器装饰的函数，正常执行会变成任务提交的功能，
    # 会将函数执行的任务提交给线程池进行执行，所以任务提交并不会卡住程序
    # 所以需要多线程操作的函数不要写 return 语句，以及尽量使用主线程中的 list 或 queue 来收集执行结果
    @pool(10) # 开启线程池组，默认名字为 'v'，线程数量为10
    def func1(a,b):
        rd = random.random(); time.sleep(rd)
        print(a+b, '{:.3f}'.format(rd))
    @pool(3,gqueue='h') # 开启线程池组，指定名字为 'h'，线程数量为3
    def func2(a,b,c):
        rd = random.random(); time.sleep(rd)
        print(a*b*c, 'hhhhhhh', '{:.3f}'.format(rd))
    for i in range(30): func1(i,i*i)   # 随便丢30个任务查看多任务多线程池执行效果
    for i in range(30): func2(i,i+i,3) # 随便丢30个任务查看多任务多线程池执行效果
    print('start wait.')
    pool.wait()  # 等待函数 func1 任务在默认的 gqueue='v' 的“线程池组”里面全部执行完
    pool.wait(gqueue='h') # 等待函数 func2 在 gqueue='h' 的“线程池组”里面全部执行完
    print('end wait.')
    # 另外 print 函数自动变成输入带有线程名字前缀的、带有锁的函数