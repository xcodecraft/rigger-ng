#coding=utf8
import types , re , os , string ,  getopt , pickle ,yaml  , logging
import setting
from utls.rg_io import rgio

_logger = logging.getLogger()


class rg_args :
    def __init__(self):
        self.clear()

    def clear(self):
        self.data          = os.path.abspath("./.rigger-ng.dat")
        self.conf          = os.getcwd() + "/_rg/conf.yaml"
        self.log_level     = logging.ERROR
        self.os            = None
        self.user          = None
        self.root          = os.path.dirname(os.path.realpath(__file__))
        self.root          = os.path.dirname(self.root)


class prj_args :
    def __init__(self):
        self.clear()

    def clear(self):
        self.env  = None
        self.conf = None
        self.sys  = None
        self.cmds = []
    def __str__(self) :
        cmd = "," . join(self.cmds)
        return "%s -e %s -s %s" %(cmd,self.env,self.sys)


class run_args :
    def __init__(self):
        self.rg = rg_args()
        self.prj = prj_args()


    def parse_cmd(self):
        if len(self.cmds) == 0 :
            raise badargs_exception("æ²¡æå½ä»¤")
        if len(self.cmds) > 1:
            self.subcmd = self.cmds[1:]
            _logger.info("subcmd: %s" %self.subcmd)
        cmdarr = self.cmds[0].split(',')
        return cmdarr

    @staticmethod
    def load():
        rargs     = run_args()
        data_file = rargs.rg.data
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
        data_file = self.rg.data
        with open(data_file,'w')  as f:
            pickle.dump(self, f)

    def __str__(self):
        info = str(self.prj)
        return  info
    @staticmethod
    def help():
        # rgio.prompt("rg  <dev cmd>   [-m <message>] ")
        rgio.prompt("rg  <svc cmd>   [-e <env>]     [-s <system>]   [-x <resource>]  [-f <script>]    [-v <vardef>]")
        # rgio.prompt("rg  <pub cmd>   [-p <project>] [-l <publish plan> ]  [-h [@|%]<host>] [-t [@]<tag>] [-z <rguser> ]")
        # rgio.prompt("rg  <batch cmd> [-p <project>] [-l <publish plan> ]  [-h [@|%]<host>] [-t [@]<tag>] [-z <rguser> ]")
        rgio.prompt("\ncommon args : [-d <level> ]\n")


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
            setting.debug_level =  int(self.argv['-D'])
        if self.argv.has_key('-d')   :
            setting.debug_level =  int(self.argv['-d'])
        return debug

    def parse(self,rargs,argv):

        status = self.ST_NEXT
        key    = ""
        val    = None
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
                        rargs.prj.cmds.append(item)
                        # rargs.cmds.append(item)
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
            rargs.rg.conf  = self.argv['-c']
        if self.argv.has_key('-z'):
            rargs.rg.user  =self.argv['-z']
        if self.argv.has_key('-e'):
            rargs.prj.env =self.argv['-e']
        if self.argv.has_key('-o'):
            rargs.rg.os =self.argv['-o']
        if self.argv.has_key('-s'):
            rargs.prj.sys =self.argv['-s']
