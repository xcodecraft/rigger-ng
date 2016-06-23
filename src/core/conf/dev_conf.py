#coding=utf-8
import  os , string   , logging ,re ,sys
import  interface,utls.rg_sh

from utls.rg_io import rgio ,rg_logger
from string     import Template
from define     import *
import  utls.check , utls.dbc , utls.rg_sh

from utls.pattern  import  fail_exception 

import ConfigParser


class project(interface.rg_conf.base,singleton):
    name = ""
    root = ""
    def __init__(self):
        self.root = utls.rg_var.value_of(self.root)
        pass
    @staticmethod
    def ins():
        return singleton.get_ins(project)



class version (interface.rg_conf.base,singleton):
    file = None
    # first  = 0
    # second = 1
    # third  = 0
    # forth  = 0
    @staticmethod
    def ins():
        return singleton.get_ins(version)
    def __init__(self):
        # import  pdb
        # pdb.set_trace()
        utls.check.must_true(os.path.exists(self.file),"version file not exists : %s" %(self.file ))
        file=open(self.file)
        line=file.readline()
        file.close()
        res=re.match(r"(\d+)\.(\d+)\.(\d+)\.(\d+)",line)
        utls.check.ok(res,"bad version: %s " %line)
        intdata=[]
        for str in res.groups():
            intdata.append(int(str))
        self.first,self.second,self.third,self.forth=intdata

    def up_commit(self):
        self.forth += 1
    def up_bugfix(self):
        self.third +=1
    def up_feature(self):
        self.second +=1
        self.third  = 0
    def up_struct(self):
        self.second = 0
        self.third  = 0
        self.first += 1
    def save(self):
        file=open(self.file,'w')
        data="%d.%d.%d.%d" %(self.first,self.second,self.third,self.forth)
        file.write(data)
        file.close()
    def info(self):
        return "%d.%d.%d.%d" %(self.first,self.second,self.third,self.forth)
    def digitver(self):
        return  self.first * 10000  + self.second * 100  + self.third

    def is_compatible(self,beg,end):
        return self.digitver() >= beg.digitver() and self.digitver() <= end.digitver()
    def update_ver(self):
        old_ver = self.info()
        chose_update_version="plese chose  working(w), fixbug(b), add feature(f) , struct revolution(s)  ?"
        print(chose_update_version)
        recomTag   = False
        needCommit = False
        chose      = sys.stdin.read(1)
        if chose == "w":
            self.up_commit()
            pass
        if chose == "b":
            self.up_bugfix()
            self.up_commit()
        if chose == "f":
            self.up_feature()
            self.up_commit()
        if chose == "s":
            self.up_struct()
            self.up_commit()
        self.save()
        rgio.prompt("version updated : [$OLD] ---> [$NEW]",OLD=old_ver,NEW=self.info())


class git (interface.rg_conf.base,singleton) :
    remote = ""
    def __init__(self):
        pass
    @staticmethod
    def ins():
        return singleton.get_ins(git)

    def fetch_project(self,local,prj,tag=None):
        prjs_root = local
        prj_path  = prjs_root + "/" + prj
        if os.path.exists(prj_path):
            cmd = " cd $PRJS_ROOT/$PRJ; git fetch ;  "
        else:
            cmd = " cd $PRJS_ROOT ; git clone $G$PRJ.git ; cd $PRJ; "
        if not  tag is None:
            cmd += " git checkout $TAG;"
        cmd = Template(cmd).substitute(G=self.remote,PRJ=prj,TAG=tag , PRJS_ROOT=prjs_root )
        print "git cmd:" + cmd;
        code = self.execmd(cmd,True)
        print("code:%s" % code)
        pass
    def chose_tag(self,local,prj,tag=None ):
        prjs_root = local
        last_tag_file   =  prjs_root + "/" +  prj + "_last.tags"
        re_tag_file     =  prjs_root + "/" +  prj + "_re.tags"
        rc_tag_file     =  prjs_root + "/" +  prj + "_rc.tags"
        cmd = """
            cd $PRJS_ROOT/$PRJ ;
            git tag | $FILTER sort  -t. -k4 -g -r | head -n 5 > $OUT0;
            git tag | $FILTER grep -E '[0-9]+\.[0-9]*[02468]\.[0-9]+\.[0-9]+'  |  sort  -t. -k4 -g -r | head -n 15 > $OUT1;
            git tag | $FILTER grep -E '[0-9]+\.[0-9]*[13579]\.[0-9]+\.[0-9]+'  |  sort  -t. -k4 -g -r | head -n 15 > $OUT2;
        """
        tfilter = ""
        if tag is not None :
            tfilter = " grep  -E \"^" + tag + "\" | "
        cmd = Template(cmd).substitute(PRJ=prj,PRJS_ROOT=prjs_root , OUT0=last_tag_file,
                OUT1=re_tag_file,OUT2=rc_tag_file,FILTER=tfilter)
        self.execmd(cmd,True)
        last_tags   = open(last_tag_file,'r') .readlines()
        re_tags     = open(re_tag_file,  'r') .readlines()
        rc_tags     = open(rc_tag_file,  'r') .readlines()
        all_tag_file = prjs_root + "/" +  prj + "_*.tags"
        self.execmd(Template("rm $TMP").substitute(TMP=all_tag_file))

        #TODO : temp implment
        count = len(last_tags)
        if count == 1 :
            return last_tags[0].strip()

        block={}
        block[0]                            = "æè¿tags:"
        block[len(last_tags)]               = "release tags:"
        block[len(last_tags)+len(re_tags)]  = "develop tags:"
        all_tags = last_tags  + re_tags + rc_tags
        index = 1
        line  = ""
        line_index = 0
        for tag in all_tags:
            tag = tag.strip()
            if index-1 in block or line_index == 5 :
                print(line)
                line = "\t"
                line_index =  0
                if index -1 in block :
                    print("\n" + block[index-1])
            line = line + "(%-2d) %-20s" %(index,tag)
            index += 1
            line_index +=1
        print(line)

        chose_key = get_chose_index("Please Chose Tag ",index-1)
        if chose_key is None:
            return None
        return all_tags[chose_key -1 ].strip()
    def checkout(self,local,prj,tag):
        prjs_root = local
        cmd = "cd $PRJS_ROOT/$PRJ ; git checkout $TAG ; "
        cmd = Template(cmd).substitute(G=self.remote,PRJ=prj,TAG=tag , PRJS_ROOT=prjs_root )
        self.execmd(cmd,True)

    def set_tag(self,ver):
        cmd = "git tag $VER; git push --tags "
        cmd = Template(cmd).substitute(VER=ver)
        self.execmd(cmd,True)
    def commit(self,ver,message):
        cmd = """git commit -a -m "$MSG" """
        cimsg = "[" + ver  + "]"
        if message is not None:
            cimsg  = cimsg + " " +  message
        cmd = Template(cmd).substitute(MSG=cimsg)
        self.execmd(cmd,True,[0,256])
    def push(self):
        cmd="""GIT_POOL=`git remote -v  | grep push | awk '{print $2}' ` ; CUR_BRANCH=`git branch | grep \* | awk '{print $2}'`; git pull $GIT_POOL $CUR_BRANCH ; git push $GIT_POOL $CUR_BRANCH ; """
        self.execmd(cmd,True)

    def tag_release(self,local,prj,ori):
        info = "Will tag relase [ r"+ori +  "],Please input  tag message:"
        msg = get_input_line(info)
        cmd = """cd $PRJS_ROOT/$PRJ ;  git tag -a -m "$MSG" r$TAG $TAG ; git push --tags """
        cmd = Template(cmd).substitute(PRJ=prj,PRJS_ROOT=local,TAG=ori,MSG=msg)
        self.execmd(cmd,True)


class sonar(interface.rg_conf.base,singleton):
    """
    - !C.sonar
        runner   : "/data/x/tools/sonar/bin/sonar-runner"
        qube     : "http://xxxx"
        src      : "src"
        language : "php"
        config   : 
            - ""
    """
    def __init__(self) :
        self.prjname  = project.ins().name
        self.version  = version.ins().info()
        if len(self.qube) > 0 :
            self.qube  = "sonar.host.url= " +  self.qube 
        # self.version  = "1.0.0.0"
        # self.src      = self.src
        # self.language = utls.rg_var.value_of(self.language)
        # self.dstpath  = utls.rg_var.value_of(self.dstpath)

    @staticmethod
    def ins():
        with   fail_exception(interface.rigger_exception("bad sonar conf "))  :
            return singleton.get_ins(sonar)

    def run(self) :
        # root  = os.path.join(project.ins().root , "sonar-project.properties")
        cmd = "cd $PRJ_ROOT; $RUNNER "
        cmd = Template(cmd).substitute(PRJ_ROOT = project.ins().root , RUNNER = self.runner)
        code = self.execmd(cmd,True)
    def build_file(self):
        content="""
        ${QUBE}
        sonar.projectKey=${PRJ_NAME}
        sonar.projectName=${PRJ_NAME}
        sonar.projectVersion=${PRJ_VER}
        sonar.sources=${PRJ_SRC}
        sonar.language=${PRJ_LANG}
        sonar.sourceEncoding=UTF-8
        """

        c = Template(content).substitute(QUBE=self.qube,PRJ_NAME=self.prjname, PRJ_VER=self.version,
                PRJ_SRC=self.src,PRJ_LANG=self.language)
        conf = os.path.join(project.ins().root , "sonar-project.properties")
        with  open(conf ,'w') as f :
            f.write(c)
            if hasattr(self,"config") :
                for line in self.config:
                    f.write(line + "\n")
