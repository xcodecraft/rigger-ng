#coding=utf-8
import string , logging , re
import rg_err

class base:
    def obj_has(self,key):
        return self.__dict__.has_key(key)
    def cls_has(self,key):
        return self.__class__.__dict__.has_key(key)
    def echo(self,output):
        name = str(self.__class__)
        output("\n!R.%s" %name)
        attrs = self.__dict__
        for a,v in attrs.items() :
            if  a == "__module__"  or a == "__doc__" :
                continue
            if re.match(r'^_\w+',a):
                a = a[1:]
            if isinstance(v,str) :
                output('\t %-15s : "%s" ' %(a,v))
            if v is None:
                output('\t %-15s : None ' %(a))
            if isinstance(v,list):
                output('\t %-15s : [] ' %(a))
            if isinstance(v,bool):
                output('\t %-15s : %s ' %(a,v))

    def useage(self,output):
        attrs = self.__class__.__dict__
        name = str(self.__class__)
        output("\n!R.%s" %name)
        if hasattr(self, '__doc__') and self.__doc__ is not None:
            output(self.__doc__)

        output("property:" )
        for a,v in attrs.items() :
            if  a == "__module__"  or a == "__doc__" :
                continue
            if re.match(r'^_\w+',a):
                a = a[1:]
            if isinstance(v,str) :
                output('\t %-15s : "%s" ' %(a,v))
            if v is None:
                output('\t %-15s : None ' %(a))
            if isinstance(v,list):
                output('\t %-15s : [] ' %(a))
            if isinstance(v,bool):
                output('\t %-15s : %s ' %(a,v))

    def __getattr__(self,key):
        cls_name = self.__class__.__name__
        raise rg_err.rigger_exception("'%s' 没有 '%s' 属性" %(cls_name,key))