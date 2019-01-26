# 增加环境变量，仅测试使用
import os
import sys
p = os.path.split(os.getcwd())[0]
sys.path.append(p)
import sys;print(sys.stdout.encoding)


from vrequest import main
main.execute()