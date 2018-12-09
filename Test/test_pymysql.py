import sys, os

print(sys.path)
workpath = os.path.dirname(os.path.abspath(sys.argv[0]))
sys.path.insert(0, os.path.join(workpath, 'modules'))
print(sys.path)

import pymysql