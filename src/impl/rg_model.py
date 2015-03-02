#coding=utf-8
import string , logging, sys
import interface
import utls.rg_io ,utls.rg_sh
_logger = logging.getLogger()



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
