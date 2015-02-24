import  re , os , string ,  getopt ,sys , unittest,logging

root  = os.path.dirname(os.path.realpath(__file__))
root  = os.path.dirname(root)
sys.path.append(os.path.join(root,"src") )
sys.path.append(os.path.join(root,"test") )

from testcase.core_tc  import *
from testcase.yaml_tc  import *
from testcase.tpl_tc   import *
from testcase.vars_tc  import *


if __name__ == '__main__':
    unittest.main()
