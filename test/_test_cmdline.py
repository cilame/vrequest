# 增加环境变量，仅测试使用
import os
import sys
p = os.path.split(os.getcwd())[0]
sys.path.append(p)
import sys;print(sys.stdout.encoding)


try:
    # 处理 sublime 执行时输出乱码
    import io
    import sys
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
    sys.stdout._CHUNK_SIZE = 1
except:
    pass


from vrequest import main
main.execute()