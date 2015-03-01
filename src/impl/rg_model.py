#coding=utf-8
import string , logging, sys
import interface
import utls.rg_io ,utls.rg_sh
_logger = logging.getLogger()


class res_runner:
    def __init__(self,res) :
        self.res = res

    @staticmethod
    def tpl_call(name,res,fun,context) :
        with utls.rg_io.scope_iotag(res._resname(),name,res._info()) :
            if res._allow(context) :
                with utls.rg_sh.scope_sudo(res.sudo) :
                    res._before(context)
                    fun(context)
                    res._after(context)

    def start(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._start,context)

    def stop(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._stop,context)

    def config(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._config,context)

    def data(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._data,context)


    def check(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._check,context)

    def clean(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._clean,context)
    def reload(self,context):
        name=sys._getframe().f_code.co_name
        res_runner.tpl_call(name,self.res, self.res._reload,context)







# class resouce_factory:
#     builders ={}
#     def register(self,res_type,builder):
#         self.builders[res_type] = builder
#     def build(self,res_type, data):
#         if self.builders.has_key(res_type) :
#             builder = self.builders[res_type]
#             return builder(data)
#         return None
#
# res_admin = resouce_factory()

# def __init__():
#     res_admin.register("system",system.load)
#     pass
