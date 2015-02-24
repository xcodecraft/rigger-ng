#coding=utf8
import types , re , os , string ,  getopt , pickle ,yaml  , logging
#import res,rigger,pubdef,cmds
from  dev import * 

_logger = logging.getLogger()

class rarg_parser:
    ST_NEXT     = 0
    ST_CMD      = 1
    ST_ARG_KEY  = 3
    ST_ARG_VAL  = 4
    def __init__(self):
        self.argv  = {}

    def load_args(self,saved ) :
        if hasattr(saved,'vars_def') and saved.vars_def is not None:
            if not self.argv.has_key('-v') :
                self.argv['-v'] = saved.vars_def
            else:
                _logger.info ( "old prior vars ignore:  %s " % rargs.vars_def)

    def debug_level(self):
        debug = 0 
        if self.argv.has_key('-D')   :
            debug   =  int(self.argv['-D'])
        if self.argv.has_key('-d')   :
            debug   =  int(self.argv['-d'])
        return debug 

    def parse(self,rargs,argv):
        
        status = self.ST_NEXT
        key = ""
        val = None
        for item in argv :
            item = item.strip()
            while True:
                if status == self.ST_ARG_VAL:
                    if re.match(r'-\w+',item) :
                        status  = self.ST_NEXT  
                        continue
                    val = item
#                    print("%s:%s" %(key,val))
                    self.argv[key] = val 
                    status  = self.ST_NEXT  
                    break;
                if status == self.ST_ARG_KEY:
                    key = item
                    status = self.ST_ARG_VAL
                    break;
                if status == self.ST_CMD:
                    if len(item.strip()) > 0:
                        rargs.cmds.append(item)
                    status  = self.ST_NEXT  
                    break;
                if status == self.ST_NEXT :
                    if re.match(r'-\w\S+',item) :
                        key = item[0:2]
                        val = item[2:]
                        self.argv[key] = val 
                        status  = self.ST_NEXT  
                        break;
                    elif re.match(r'-\w',item) :
                        status = self.ST_ARG_KEY
                    else :
                        status = self.ST_CMD

        if self.argv.has_key('-c') :
            rargs.conf = self.argv['-c']
        if self.argv.has_key('-z'):
            rargs.rg_user =self.argv['-z']

class empty_var:
    def __init__(self,key):
        self.key  = key
    def __str__(self):
        return ""
class runargs : 
    env         = None
    prj         = None
    sysname     = None
#    vars_def    = empty_var('-v')
    def __init__(self):
        self.clear()
        self.is_config     = False
        self.os_env        = "diy"
        self.message       = ""
        self.script        = None
        self.rg_root       = (os.path.dirname(os.path.realpath(__file__)) + "/../")
        self.version       =  version(os.path.join(self.rg_root ,"version.txt" ))
        self.compatible    = False
        self.var_defs      = None
        self.stdin         =  []
        self.rg_user       = None  

    def clear(self):
        self.data          = os.path.abspath("./.rigger.dat")
        self.prj           = os.path.basename(os.getcwd())
        self.conf          = os.getcwd() + "/_rg/conf.yaml"
        self.log_level     = logging.ERROR
        self.prj           = None
        self.git           = None
        self.user          = None
        self.tag           = None
        self.message       = ""
        self.rg_root       = (os.path.dirname(os.path.realpath(__file__)) + "/../")
        self.cmds          = []
        self.allow_res     = "ALL"
        self.batch         = False
        self.publish       = None
        self.subcmd        = None
        self.host          = None
        self.script        = None
        self.devtest       = False
        self.force         = True
        self.rg_root       = (os.path.dirname(os.path.realpath(__file__)) + "/../")
        self.version       = version(os.path.join(self.rg_root ,"version.txt" ))

    def run_check(self):
        if self.os_env   is None:
            print("no env is setting!" )
            return False
        return True
    @staticmethod
    def data_path():
        return os.path.abspath("./.rigger.dat")

    def parse_cmd(self):
        if len(self.cmds) == 0 :
            raise badargs_exception("没有命令")
        if len(self.cmds) > 1: 
            self.subcmd = self.cmds[1:]
            _logger.info("subcmd: %s" %self.subcmd)
        cmdarr = self.cmds[0].split(',')
        return cmdarr 

    @staticmethod 
    def load():
        rargs = runargs()  
        data_file = rargs.data_path()
        rargs.compatible = False
        if os.path.exists(data_file):
            try:
                with open(data_file,'r')  as f: 
                    rargs = pickle.load(f)
                    rargs.compatible = False
            except Exception as  e :
                rgio.prompt("load rigger file fail!")
            if hasattr(rargs,'version'):
                rargs.compatible = rargs.version.is_compatible(version(verstr="0.8.0.0"),version(verstr="1.0.0.0"))

        rargs.clear()
        return rargs
    def save(self):
        data_file = self.data_path()
        with open(data_file,'w')  as f: 
            pickle.dump(self, f)

    def __str__(self):
        info = "conf: "
        if self.sysname is not None:
            info += " -s " + self.sysname 
        if self.env  is not None:
            info += " -e " + self.env 
        if self.os_env is not None:
            info += " -o " + self.os_env 
        if hasattr(self,'vars_def') and self.vars_def is not None:
            info += " -v " + self.vars_def
        return  info
    @staticmethod
    def help():
        rgio.prompt("rg  <dev cmd>   [-m <message>] ")
        rgio.prompt("rg  <svc cmd>   [-e <env>]     [-s <system>]   [-x <resource>]  [-f <script>]    [-v <vardef>]")
        rgio.prompt("rg  <pub cmd>   [-p <project>] [-l <publish plan> ]  [-h [@|%]<host>] [-t [@]<tag>] [-z <rguser> ]")
        rgio.prompt("rg  <batch cmd> [-p <project>] [-l <publish plan> ]  [-h [@|%]<host>] [-t [@]<tag>] [-z <rguser> ]")
        rgio.prompt("common args : [-d <level> ]")
