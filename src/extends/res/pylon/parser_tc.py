import  utls.tpl ,interface ,base.tc_tools
# import  impl.rg_args , impl.rg_run
import  os

from  parser import  *


class parser_tc(base.tc_tools.rigger_tc):

    def test_parse_cls(self):

        curdir  = os.path.dirname(os.path.realpath(__file__))
        curdir  = os.path.join(curdir,"data")
        src     = os.path.join(curdir,"example.php")
        clsdst  = os.path.join(curdir,"clsdst.out")
        pathdst = os.path.join(curdir,"pathdst.out")
        expect  = os.path.join(curdir,"clspath.expect")

        parser = php_class_parser()
        with   open(pathdst,'w') as pathobj , open(clsdst,'w') as clsobj:
            parser.parse_file(src,"",pathobj,clsobj)

        self.assertMacroFile(pathdst,expect)

    def test_parse_rest(self):

        curdir = os.path.dirname(os.path.realpath(__file__))
        curdir = os.path.join(curdir,"data")
        src    = os.path.join(curdir,"rest.php")
        dst    = os.path.join(curdir,"restdst.out")
        expect = os.path.join(curdir,"rest.expect")

        parser = php_rest_parser()
        with   open(dst,'w') as dstobj :
            parser.parse_file(src,dstobj,2)

        self.assertMacroFile(dst,expect)
