#coding=utf8
import re
import interface , rg_var , rg_model

class res_box(interface.resource):

    def __init__(self):
        self.res = []
    # res = []
    def items_call(self,fun,context):
        if self._allow(context):
            for r in self.res :
                run = rg_model.res_runner(r)
                fun(run,context)

    def _start(self,context):
        self.items_call(rg_model.res_runner.start,context)

    def _stop(self,context):
        self.items_call(rg_model.res_runner.stop,context)

    def _config(self,context):
        self.items_call(rg_model.res_runner.config,context)
    def _data(self,context):
        self.items_call(rg_model.res_runner.data,context)
    def _check(self,context):
        self.items_call(rg_model.res_runner.check,context)

    def _reload(self,context):
        self.items_call(rg_model.res_runner.reload,context)
    def _clean(self,context):
        self.items_call(rg_model.res_runner.clean,context)
    def _allow(self,context):
        return True
    def append(self,item):
        self.res.append(item)
    def push(self,item):
        self.res.insert(0,item)

class system (res_box ):
    def _before(self,context):
        rg_var.keep()
        context.keep()
        pass
    def _after(self,context):
        context.rollback()
        rg_var.rollback()
        pass
    pass

class project(res_box) :
    pass

class module(res_box) :
    pass


class env(interface.resource):
    def _resname(self):
        if hasattr(self,'name'):
            return  "%s(%s)" %(self._clsname(),self.name)
        return self._clsname()


class vars(interface.resource):
    """
    å®ä¹ç¯å¢åé:
    !R.vars:
        A: 1
        B: "hello"
    """


    def depend_check(self,context) :
        pass

    def _allow(self,context):
        return True
    def _before(self,context):
        items = self.__dict__

        for name , val in   items.items():
            if re.match(r'__.+__',name):
                continue
            name= name.upper()
            setattr(context,name,val)
        rg_var.import_dict(items)

class echo(interface.resource) :
    """
        !R.echo :
            value : "${PRJ_ROOT}"
    """
    def _allow(self,context):
        return True
    def _before(self,context):
        pass
    def _config(self,context):
        v = rg_var.value_of(self.value)
        print("echo,vlaue: %s " %(v))

class assert_eq(interface.resource) :
    """
    !R.assert
        value  : "${APP_SYS}"
        expect : "test"
    """
    def _allow(self,context):
        return True
    def _config(self,context):
        self.assert_eq(context)
    def assert_eq(self,context):
        value  = rg_var.value_of(self.value)
        expect = rg_var.value_of(self.expect)
        if value != expect :
            raise interface.rigger_exception("value: %s , expect : %s " %(value,expect))
    def _start(self,context) :
        self.assert_eq(context)

