#coding=utf8
import  logging
from base.tc_tools   import *
import  utls.tpl
import  interface
import  utls.rg_var
from utls.tpl.tpl_var import *
_logger = logging.getLogger()



class exp_tc(rigger_tc):
    def test_exp(self):
        context = interface.run_context()
        context.need_admin = "TRUE"
        context.mode       = "rest"

        utls.rg_var.clean()
        utls.rg_var.import_context(context)
        v = utls.rg_var.value_of("${MODE}")
        self.assertEqual(v,'rest')

        utls.rg_var.clean()

class porp_tc(rigger_tc) :
    def test_simple(self):
        a   = attr_proxy(icase_porp())
        a.x = 1
        a.y = 2
        self.assertEqual(a.x, 1)
        self.assertEqual(a.y, 2)

    def test_combo(self) :
        a = attr_proxy(icase_porp())
        b = attr_proxy(icase_porp())
        a.x = 1
        a.y = 2
        b.x = 3
        b.y = 4

        p1 = attr_proxy(combo_porp(a,b))
        self.assertEqual(p1.x, 1)
        self.assertEqual(p1.y, 2)

        p2 = attr_proxy(combo_porp(b,a))
        self.assertEqual(p2.x, 3)
        self.assertEqual(p2.y, 4)


    @staticmethod
    def value_of_x(name):
        return 10
    @staticmethod
    def value_of_y(name):
        return 1

    def test_layzer(self) :
        # import  pdb
        # pdb.set_trace()

        funs      = {}
        funs['x'] = porp_tc.value_of_x
        funs['y'] = porp_tc.value_of_y
        p1        = attr_proxy(layzer_porp(funs))
        self.assertEqual(p1.x, 10)
        self.assertEqual(p1.y, 1)



class tpl_tc(rigger_tc):

    # def test_engine_vardict(self):
    #     context = interface.run_context()
    #     context.need_admin = "TRUE"
    #     context.mode       = "rest"
    #
    #     utls.tpl.var.clean()
    #     utls.tpl.var.import_attr(context)
    #
    #     self.engine_check()

    # def test_engine_varstr(self) :
    #     utls.tpl.var.clean()
    #     utls.tpl.var.import_str("need_admin=TRUE,mode=rest")
    #     self.engine_check()



    def test_file(self):
        base = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/utls_tc/tpl_simple")
        ngx  = utls.tpl.engine(base + "/_tpl.yaml")
        ngx.append_vars("youname=abc,love=TRUE,db=mysql")
        ngx.proc_file( base +"/example.sh", base+ "/example.out")
        self.assertMacroFile(base + "/example.out" , base + "/example.expect")

    def test_path(self):
        base     = utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/utls_tc/tpl_path")
        ngx      = utls.tpl.engine(base + "/_tpl.yaml")
        # for auto-test
        ngx.append_vars("sys_name=abc,need_mysql=TRUE")
        dst_path = ngx.proc_path(base + "/%{SYS_NAME}")
        self.assertEqual(dst_path, base + "/abc")
        dst_path = ngx.proc_path(base + "/%{NEED_MYSQL}/mysql")
        self.assertEqual(dst_path, base + "//mysql")
        dst_path = ngx.proc_path(base + "/%{SYS_NAME}_data")
        self.assertEqual(dst_path, base + "/abc_data")



    # def test_cmd(self):
    #     root      = os.getcwd() + "/test"
    #     run_rigger("tpl %s/tpl/ori/ -o %s/out/ -v host=192.168.0.1,sdk_pkg=True,xshell=FALSE,HELLO=nohello  "  %(root,root))
    #     run_rigger("tpl %s/tpl/ori/single.sh -o %s/out/single.sh -v HELLO=hello "  %(root,root))
    #     self.out_root = "%s/out" %root
    #     self.assertDir(self.out_root , "%s/expect" %root)

    # def test_res(self):
    #     run_rigger("conf  -s tpl_res -e dev  -v host=192.168.0.1,sdk_pkg=True,xshell=FALSE  " )
    #     root      = os.getcwd() + "/test/"
    #     self.assertDir(root+ "tmp/outres", root + "expect")
