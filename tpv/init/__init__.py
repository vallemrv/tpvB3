import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname+'/../../')
sys.path.append(dname+'/../../')
