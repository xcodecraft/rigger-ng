#coding=utf8
import  logging
# import  re , os , string ,  getopt ,sys , unittest,logging
from base.tc_tools   import *
import  utls.tpl
import  interface
import  impl.rg_var

_logger = logging.getLogger()



class exp_tc(rigger_tc):
    def test_exp(self):
        context = interface.run_context()
        context.need_admin = "TRUE"
        context.mode       = "rest"

        impl.rg_var.clean()
        impl.rg_var.import_context(context)
        v = impl.rg_var.value_of("${MODE}")
        self.assertEqual(v,'rest')

        #测试找不到行为
        impl.rg_var.clean()
        v = impl.rg_var.value_of("${MODE}")
        # self.assertEqual(v,'__NOFOUND_[MODE]__')


class tpl_tc(rigger_tc):

    def test_engine_vardict(self):
        context = interface.run_context()
        context.need_admin = "TRUE"
        context.mode       = "rest"

        utls.tpl.var.clean()
        utls.tpl.var.import_dict(context.__dict__)

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
    def assertDir(self,first,second):
        root = {}
        root['fst'] = first
        root['sec'] = second
        os.path.walk(first,self.proc_file,root)
        pass

    def proc_file(self,root,dirname,names):
        src_path = dirname
        dst_path = root['sec'] + src_path.replace(root['fst'],'')
        for n in names:
            src = os.path.join(src_path ,n)
            dst = os.path.join(dst_path ,n)
            if  os.path.isdir(src):
                continue

            if not os.path.exists(dst):
                self.assertTrue(False,"dst_path %s not exists" %dst)
            src_st = os.stat(src)
            dst_st = os.stat(dst)
            self.assertEqual(src_st.st_mode,dst_st.st_mode,"file mod is diffrent! [%s]" %dst)
            src_lines       = open(src, 'r').readlines()
            dst_lines       = open(dst, 'r').readlines()
            self.maxDiff   = None
            self.assertItemsEqual(src_lines,dst_lines)


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
