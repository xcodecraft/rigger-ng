import  re , os , string ,  getopt ,sys , unittest,logging

root  = os.path.dirname(os.path.realpath(__file__))
root  = os.path.dirname(root)
sys.path.append(os.path.join(root,"src") )
# sys.path.append(os.path.join(root,"test") )

# from impl.impl  import *
from impl_tc.yaml_tc  import *
from impl_tc.tpl_tc   import *
from impl_tc.vars_tc  import *
from impl_tc.args_tc  import *
from impl_tc.cmd_tc   import *

# from res_tc.mysql_tc import *

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    _logger = logging.getLogger()
    # file_handler = logging.FileHandler("test.log")
    # file_handler.setFormatter(formatter)
    # _logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler(sys.stderr)
    _logger.addHandler(stream_handler)
    # _logger.info("hello")
    unittest.main()
