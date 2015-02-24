import  re , os , string ,  getopt ,sys , unittest,logging

# import  rigger,rg_pub.pubdef,rg_run
# from  rargs     import *
# from  rg_sh     import *
# from  dev       import *
#from  pub.publish   import *

#def run_rigger(rargs):

# run_os = "diy"
# prj_root = "devspace/rigger"
#
# def path_of_prj(path="") :
#     if len( path ) == 0 :
#         return "%s/devspace/rigger" %(os.environ['HOME'])
#     return "%s/devspace/rigger/%s" %(os.environ['HOME'],path)
#
# def run_rigger(args_str):
#
#     rargs = runargs()
#     rargs.clear()
#     rargs.conf       = os.getcwd() + "/test/prj/_rg/conf.yaml"
#     rargs.compatible = True
#     rargs.rg_user    = "zuowenjian"
#     args_str = args_str +  " -o %s " % run_os
#     rg_run.main_impl(rargs,args_str.split(' '))


class shexec_mock:
    def cond(self,cmd,tag):
        pass
    def intercept(self,cmd,check,okcode):
        pass
    def __enter__(self):
        self.cmds      = ""
        shexec.cond_exec(self.cond,self.intercept)
        pass
    def __exit__(self, exc_type, exc_value, traceback ):
        shexec.clear_cond_exec()
        pass


class rigger_tc(unittest.TestCase):
    pass
    # def format_data(self,arr,ignrexs):
    #     out=[];
    #     for line in arr:
    #         for ign in ignrexs:
    #             line = re.sub(ign,'',line)
    #         line = line.strip()
    #         if len(line)  > 0 :
    #             out.append(line)
    #     return out
    # def assertTextEqual(self,first,second,ignrexs=[],debug=False):
    #     ignrexs.append(r'\d+\.\d+\.\d+\.\d+')
    #     fst_arr  = self.format_data(first.split('\n'),ignrexs)
    #     sec_arr  = self.format_data(second.split('\n'),ignrexs)
    #     self.assertItemsEqual(fst_arr,sec_arr)
    #
    # def macro_data(self,arr):
    #     out = []
    #     for line in arr :
    #         line = env_exp.value(line.strip())
    #         if len(line)  > 0 :
    #             out.append(line)
    #     return out
    #
    # def assertMacroEqual(self,first,second):
    #     os.environ['RIGGER_ROOT'] = path_of_prj("")
    #     fst_arr  = self.macro_data(first.split('\n'))
    #     sec_arr  = self.macro_data(second.split('\n'))
    #     self.assertListEqual(fst_arr,sec_arr)
    #
    # def assertFileEqual(self,first,second):
    #     first_arr  = []
    #     second_arr = []
    #     with open(first) as  first_file :
    #         first_arr = first_file.readlines()
    #     with open(second) as  second_file :
    #         second_arr = second_file.readlines()
    #     self.assertItemsEqual(first_arr,second_arr)
    #
    # def assertMacroFile(self,first,second):
    #     first_arr  = []
    #     second_arr = []
    #     with open(first) as  first_file :
    #         first_arr = first_file.readlines()
    #     with open(second) as  second_file :
    #         second_arr = second_file.readlines()
    #     self.assertItemsEqual(self.macro_data(first_arr),self.macro_data(second_arr))

# class res_tc_base(rigger_tc):
#     def setUp(self):
#         self.maxDiff =None
#         self.expect_header =""" """
#         ignore_home     = os.environ['HOME']
#         ignore_touch    =  r"touch .*"
#         self.ignore_arr = [ignore_home,r".* mkdir -p .+/run.*;"
#                 , r".* mkdir -p .+/log.*"
#                 ]
