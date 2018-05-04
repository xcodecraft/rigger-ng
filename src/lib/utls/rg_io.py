#coding=utf8
import  re , os , sys, logging ,string
from string  import Template
import  setting,interface
import  utls.pattern

class run_struct:
    trace   = []
    @staticmethod
    def push(resname):
        run_struct.trace.append(resname)
    @staticmethod
    def pop():
        run_struct.trace.pop()

# class rg_logger(utls.pattern.singleton) :
class rg_logger :
    struct_out = True

    @staticmethod
    def struct_tab():
        tab = ""
        for c in run_struct.trace :
            tab = tab + "\t"
        return tab
    @staticmethod
    def debug(message) :
        logger = logging.getLogger()
        tab    = rg_logger.struct_tab()
        logger.debug(tab + message)

    @staticmethod
    def info(message) :
        logger = logging.getLogger()
        tab    = rg_logger.struct_tab()
        logger.info(tab + message)

    @staticmethod
    def warning(message) :
        logger = logging.getLogger()
        tab    = rg_logger.struct_tab()
        logger.info(tab + message)

    @staticmethod
    def error(message) :
        logger = logging.getLogger()
        tab    = rg_logger.struct_tab()
        logger.error(tab + str(message))

class prompt:
    @staticmethod
    def recommend(find, keys):
        find_len = len(find)
        wordlen =3
        if find_len >=13 :
            wordlen=5
        if find_len >=9 :
            wordlen=4
        recommend = []
        beg=0
        for x in range(wordlen-1,find_len,wordlen):
            end=x+1
            pice=find[beg:end]
            if len(pice) < 2:
                    continue;
            recommend  = recommend +  prompt.match(pice,keys)
            beg=end
        return recommend
    @staticmethod
    def match(find ,keys):
        match=[]
        if len(find) > 0  :
            for key in keys:
                if re.compile(find).search(key):
                    match.append(key)
        return match;



class scope_iotag :
    tags = []
    def __init__(self,res,tag):
        self.res = res
        self.tag = tag
    def __enter__(self):
        rgio.catch_start()
        rgio.has_err = False
        trace        = string.join(rgio.trace,'.')
        rg_logger.info("%s.%s" %(self.res,self.tag))

    def __exit__(self, exc_type, exc_value, traceback ):
        out = rgio.buf
        rgio.catch_end()
        if setting.debug  or rgio.has_err :
            if out  is not None and len(out) > 0 :
                rg_logger.error(out)
            else:
                pass
        rgio.has_err   = False

class rgio:
    buf     = None
    has_err = False
    trace   = []
    logger  = None

    @staticmethod
    def using_logger(l):
        rgio.logger =  l


    @staticmethod
    def push_trace(resname):
        rgio.trace.append(resname)


    @staticmethod
    def pop_trace():
        rgio.trace.pop()
    @staticmethod
    def catch_start():
        rgio.buf = ""
    @staticmethod
    def catch_end():
        rgio.buf = None

    @staticmethod
    def list2str(lst):
        s = ""
        for v in lst :
            if len(s) == 0 :
                s =  str(v)
            else:
                s = s + "," +  str(v)
        return s
    @staticmethod
    def prompt(*args,**kws):
        msg=args[0]
        settingo = Template(msg).substitute(kws)
        if rgio.buf is not None:
            rgio.buf  += settingo  + "\n"
        else:
            print(settingo)
            rg_logger.error(settingo)


    @staticmethod
    def inred( s ):
        return "%s[31;2m%s%s[0m"%(chr(27), s, chr(27))

    @staticmethod
    def error(msg):
        if rgio.buf is not None:
            rgio.buf  += msg  + "\n"
        rgio.has_err   = True
        print( rgio.inred(msg))
        rg_logger.error(msg)

    @staticmethod
    def simple_out(msg):
        if rgio.buf is not None:
            rgio.buf  += msg + "\n"
        else:
            print(msg)
            rg_logger.info(msg)

    @staticmethod
    def struct_out(msg,level=0):
        tab = ""
        for c in run_struct.trace :
            tab = tab + "\t"
        for i in range(level) :
            tab = tab + "\t"
        print(tab + msg)
        pass
#class uxio:
def confirm(message):
    res = get_input_line(message + "(y/n)")
    return  res.strip().lower()== 'y'
def getchose(message,quit='q',check=None):
    while True:
        rgio.prompt(message + " Quit(" + quit +  ")" )
        import sys,tty,termios
        fd = sys.stdin.fileno()
        ch = sys.stdin.read(1)
        if ch.lower() ==  quit.lower() :
            return None
        if str.isdigit(ch):
            ch = int(ch)
            if check is None :
                return ch
            if not check is None and check(ch):
                return ch
        rgio.prompt("Input error, try again!")

class in_result:
    GOOD        =  0
    CHOSE_OTHER =  1
    QUIT        =  3
    BAD         =  9
    def __init__(self,content=None):
        self.status  = in_result.GOOD
        self.content = content

def get_input_line(message,default=None,quit='q',check=None):
    if default is None :
        print("%s exit( %s ) " %(message,quit) )
    else:
        print("%s default(%s) exit(%s) " %(message,default,quit) )

    while True:
        import sys,tty,termios
        line = sys.stdin.readline().strip()
        if  len(line) == 0 :
            if default is not None:
                return  default
            continue
        if line.lower() ==  quit.lower() :
            raise interface.user_break("You stop Input!")
#            return None
        return line.strip()



def get_chose_index(message,maxnum,quit='q'):
#    message += "å¶å®(%s)" %other
    ch = get_input_line(message,None,quit)
    if ch is None:
        return None
    if str.isdigit(ch):
        ch = int(ch)
        if ch >= 1 and ch <= maxnum :
            return ch
    rgio.prompt("è¾å¥éè¯¯ï¼è¯·éæ°è¾å¥")

def chose_item(items,name):
    index = 1
    for item in  items :
        print( str(index) + "\t: " + item)
        index += 1
    print("%d\t other %s" %(index,name))
    chose_line = get_chose_index("please chose %s" %name ,index)
    if chose_line is None:
        return  None
    chose = int(chose_line)
    if chose == index:
        other = get_input_line("please input %s" %name )
        return other
    if chose >= 1 and chose <= index :
        return  items[chose-1]
    return  None

def get_mutichose_index(message,maxnum,quit='q'):
    line = get_input_line(message,quit)
    index = []
    if line is None:
        return index
    chs = line.split(",")
    for ch in chs:
        if str.isdigit(ch):
            ch = int(ch)
            if ch >= 1 and ch <= maxnum :
                index.append(ch)
    return index



def export_objdoc(name,obj):
    if obj.__doc__ is not None :
        doc = obj.__doc__.strip()
        line = doc.split('\n')
        if len(line) <= 1 :
            rgio.simple_out("\t%-10s   %s" %(name,doc))
        else:
            rgio.simple_out("\t%s : " %(name))
            for l in line :
                rgio.simple_out("\t%-10s   %s" %("",l.strip()))
    else :
        rgio.simple_out("\t%-10s " %(name))
