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
    def macro_data(self,arr):
        out = []
        for line in arr :
            line = value_of(line.strip())
            if len(line)  > 0 :
                out.append(line)
        return out

    def assertMacroEqual(self,first,second):
        self.maxDiff = 4096
        fst_arr      = self.macro_data(first.split('\n'))
        sec_arr      = self.macro_data(second.split('\n'))
        self.assertListEqual(fst_arr,sec_arr)
    def assertMacroFile(self,first,second):
        self.maxDiff = 4096
        first_arr  = []
        second_arr = []
        with open(first) as  first_file :
            first_arr = first_file.readlines()
        with open(second) as  second_file :
            second_arr = second_file.readlines()
        first_arr  = self.macro_data(first_arr)
        second_arr = self.macro_data(second_arr)
        self.assertEqual(len(first_arr),len(second_arr))
        for i in range(len(first_arr)) :
            self.assertEqual(first_arr[i],second_arr[i])

