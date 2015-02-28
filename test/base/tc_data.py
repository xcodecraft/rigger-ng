import interface
import tc_tools

class simple_res(interface.resource) :
    call_methods = []
    def reset(self):
        self.call_methods = []
    def _allow(self,context):
        return True

    def __init__(self,name="") :
        self.name = name
        self.reset()

    def _before(self,context):
        self.call_methods.append( self.name + "_before" )
        pass
    def _after(self,context):
        self.call_methods.append( self.name + "_after" )
        pass
    def _start(self,context):
        self.call_methods.append( self.name + "_start" )
        pass
    def _stop(self,context):
        self.call_methods.append( self.name + "_stop" )
        pass
    def _reload(self,context):
        self.call_methods.append( self.name + "_reload" )
        pass
    def _config(self,context):
        self.call_methods.append(self.name + "_config")
        pass

    def _data(self,context):
        self.call_methods.append( self.name + "_data" )
        pass
    def _check(self,context):
        self.call_methods.append( self.name + "_check")
        pass
    def _clean(self,context):
        self.call_methods.append( self.name + "_clean" )
        pass
