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

class tplvar_tc(rigger_tc) :
    def test_tplvar(self) :
        var = tpl_var()
        var.import_str("a=x")
        var.import_str("b=y,c=z")

        attr_val = attr_proxy(var.impl)
        self.assertEqual(attr_val.a, 'x')
        self.assertEqual(attr_val.b, 'y')
        self.assertEqual(attr_val.c, 'z')

        var.keep()
        var.import_str("a=x1,b=y1,c=z1")
        attr_val = attr_proxy(var.impl)
        self.assertEqual(attr_val.a, 'x1')
        self.assertEqual(attr_val.b, 'y1')
        self.assertEqual(attr_val.c, 'z1')

        var.rollback()
        attr_val = attr_proxy(var.impl)
        self.assertEqual(attr_val.a, 'x')
        self.assertEqual(attr_val.b, 'y')
        self.assertEqual(attr_val.c, 'z')


class tpl_tc(rigger_tc):

    def test_engine_vardict(self):
        context = interface.run_context()
        context.need_admin = "TRUE"
        context.mode       = "rest"

        utls.tpl.var.clean()
        utls.tpl.var.import_attr(context)

        self.engine_check()

    def test_engine_varstr(self) :
        utls.tpl.var.clean()
        utls.tpl.var.import_str("need_admin=TRUE,mode=rest")
        self.engine_check()

    def engine_check(self):
        expect = "/home/abc"

        ngx    = utls.tpl.engine()
        path   = ngx.proc_path("/home/#%T.need_admin:TRUE/abc")
        self.assertEqual(expect,path)

        path   = ngx.proc_path("/home/#%T.need_admin:/abc")
        self.assertEqual(expect,path)

        path   = ngx.proc_path("home/#%T.need_admin:TRUE/abc")
        self.assertEqual("home/abc",path)

        path   = ngx.proc_path("/home/#%T.need_admin:TRUE/abc/")
        self.assertEqual("/home/abc/",path)

        path   = ngx.proc_path("/home/#%T.need_admin:lala/abc/")
        self.assertEqual(None,path)

        path   = ngx.proc_path("/home/#%T.mode")
        self.assertEqual("/home/rest",path)
        path   = ngx.proc_path("/home/#%T.mode/abcd")
        self.assertEqual("/home/rest/abcd",path)


    def test_file(self):
        base =      utls.rg_var.value_of("${HOME}/devspace/rigger-ng/test/utls_tc/tpl_simple")
        ngx  = utls.tpl.engine(base + "/_tpl.yaml")
        # ngx.proc_file( base +"/example.sh", base+ "/example.out")

    # def assertDir(self,first,second):
    #     root = {}
    #     root['fst'] = first
    #     root['sec'] = second
    #     os.path.walk(first,self.proc_file,root)
    #     pass
    #
    # def proc_file(self,root,dirname,names):
    #     src_path = dirname
    #     dst_path = root['sec'] + src_path.replace(root['fst'],'')
    #     for n in names:
    #         src = os.path.join(src_path ,n)
    #         dst = os.path.join(dst_path ,n)
    #         if  os.path.isdir(src):
    #             continue
    #
    #         if not os.path.exists(dst):
    #             self.assertTrue(False,"dst_path %s not exists" %dst)
    #         src_st = os.stat(src)
    #         dst_st = os.stat(dst)
    #         self.assertEqual(src_st.st_mode,dst_st.st_mode,"file mod is diffrent! [%s]" %dst)
    #         src_lines    = open(src, 'r').readlines()
    #         dst_lines    = open(dst, 'r').readlines()
    #         self.maxDiff = None
    #         self.assertItemsEqual(src_lines,dst_lines)


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
