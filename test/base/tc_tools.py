import  re , os , string ,  getopt ,sys , unittest,logging

from utls.rg_sh import  shexec
from utls.rg_var import  value_of

def path_of_prj(path="") :
    if len( path ) == 0 :
        return "%s/devspace/rigger-ng" %(os.environ['HOME'])
    return "%s/devspace/rigger-ng/%s" %(os.environ['HOME'],path)


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

class res_mock(shexec_mock) :
    intercept = False
    cmds      = ""
    def cond(self,cmd,tag):
        self.intercept = True
        return self.intercept

    def intercept(self,cmd,check, okcode):
        self.cmds += cmd + "\n"
        return True

class rigger_tc(unittest.TestCase):
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
    def macro_data(self,arr):
        out = []
        for line in arr :
            line = value_of(line.strip())
            if len(line)  > 0 :
                out.append(line)
        return out

    def assertMacroEqual(self,first,second):
        # os.environ['PRJ_ROOT'] = path_of_prj("")
        fst_arr  = self.macro_data(first.split('\n'))
        sec_arr  = self.macro_data(second.split('\n'))
        self.assertListEqual(fst_arr,sec_arr)
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
