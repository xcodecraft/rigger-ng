#coding=utf8
import sys,re,os,string,logging  , setting
import setting , rg_sh
from utls.rg_io import  rg_logger
# import rg_sh
# from string  import Template
# import inner


# def get_key(prompt,context = None):
#     if  context is not None and hasattr(context,'answer') and len(context.answer) >=1 :
#         return context.answer
#     import sys, tty, termios
#     fd = sys.stdin.fileno( )
#     old_settings = termios.tcgetattr(fd)
#     print(prompt)
#     try:
#         tty.setraw(fd)
#         ch = sys.stdin.read(1)
#     finally:
#         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#     return ch
#
#
#
# class force_enable:
#     force_log = None
#     def host_execute(self,args,cmd,host,*cmd_args):
#         if self.force_log is None :
#             self.force_log  = open("./rg.fail", "w")
#         if args.force :
#             try :
#                 cmd(host,*cmd_args)
#             except Exception as e:
#                 self.force_log.write(host + "\n")
#         else:
#             cmd(host,*cmd_args)




# class assginer :
#     def __init__(self,host_str,unfound_call):
#         self.host_str     = host_str
#         self.unfound_call = unfound_call
#     def assgin_value(self,match):
#         import tpl.tplvar
#         var = str(match.group(1))
#         var = var.upper()
#         while True:
#             try:
#                 val  = getattr(tpl.tplvar.var(),var)
#                 rg_logger.info("[assgin] %s:%s" %(var,val ))
#                 return val
#             except tpl.tplvar.var_undefine:
#                 if self.unfound_call == None or self.unfound_call(var) == None:
#                     val = tpl.tplvar.undefine_value(var)
#                     print( "undefine %s, in %s" %(var,self.host_str))
#                     rg_logger.error( "undefine %s, in %s" %(var,self.host_str))
#                     return val



# class remote_op:
#     def __init__(self,svr,user=None):
#         self.cur_user =  env_exp.value("${USER}")
#         self.svr      = svr
#         self.user     = user
#
#     def ssh(self,cmd):
#         if self.user == self.cur_user :
#             rcmd='ssh -c blowfish $SVR -t "$CMD"'
#         else :
#             rcmd='sudo -u $USER ssh -c blowfish $SVR -t "$CMD"'
#         rcmd=Template(rcmd).substitute(SVR=self.svr,CMD=cmd,USER=self.user )
#         rg_sh.shexec.execmd(rcmd)
#     def scp(self,file , dist="~/"):
#         if self.user == self.cur_user :
#             cmd='scp -c blowfish $FILE $SVR:$DST'
#         else :
#             cmd='sudo -u $USER scp -c blowfish $FILE $SVR:$DST'
#         cmd = Template(cmd).substitute(FILE=file,SVR=self.svr,USER=self.user,DST=dist)
#         rg_sh.shexec.execmd(cmd.replace("#USER","$USER"))
#
#
#
#
# def strtpl(*args,**kws):
#     if args is None:
#         return ""
#     msg=args[0]
#     info = Template(msg).substitute(kws)
#     return  info
#
#
#
#
# def modify_string(ori,mod):
#         modarr = mod.split(',')
#         oriarr = {}
#         i = 1
#         for x in ori.split(','):
#             oriarr[x] = "__" + str(i) + "." + x
#             i += 1
#         for v in modarr:
#             if re.match(r'~.+',v) :
#                 key = v[1:].strip()
#                 if oriarr.has_key(key):
#                     oriarr.pop(key)
#             elif re.match(r'\+.+',v) :
#                 key = v[1:].strip()
#                 oriarr[key] = "__" +  str(i) + "." + key
#
#             else:
#                 oriarr      = {}
#                 oriarr[v]   = 1
#                 oriarr.append(v)
#         out = sorted(oriarr.values())
#         result = string.join(out,',')
#         result = re.sub(r'__\d+\.','',result)
#         return result
#
#
# def writeable_path(path,_delay=False) :
#     def _impl() :
#         target = path
#         while  True  :
#             if os.path.exists(target) :
#                 if os.access(target, os.W_OK) :
#                     return target
#                 else:
#                     break
#             else :
#                 target = os.path.dirname(target)
#             if target == "/"  or target == "" or target == "."  or target == "./"  or target ==  None :
#                 break
#         return None
#     if _delay :
#         _impl.err_msg = "%s %s %s" %(path,path,path)
#         return _impl
#     return _impl()
