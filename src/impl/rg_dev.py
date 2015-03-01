#coding=utf8
import re , os , sys,   logging, time
import utls.pattern
# import res_frame , resouce ,error,rg_sh
# from   string  import Template
# from   utls    import *
# from   setting import *
# from   rigger  import *
# from   rg_io    import *
# from   lang  import patterns


_logger = logging.getLogger()

# def ensure_path(path):
#     if not os.path.exists(path) :
#         rg_sh.shexec.execmd(" mkdir -p " + path)
#     return path


class work_env (utls.pattern.singleton):
    def __init__(self):
        self.space_root = ensure_path(env_exp.value("${HOME}/rigger_publish"))
        self.space_prjs = ensure_path(self.space_root + "/projects")
        self.space_tmp  = ensure_path(self.space_root + "/tmp")
        self.space_pkgs = ensure_path(self.space_root + "/pkgs")
        pass
    @staticmethod
    def scm(rargs=None):
        repository = env_exp.value("${G}")  + ":"
        if rargs is not None:
            if hasattr(rargs,"repository") and rargs.repository is not None: # git@git.corp.qihoo.net:pc-game-platform/
                repository = rargs.repository
        return git(repository)
    def fetch_project(self,rargs):
        work_env.scm(rargs).fetch_project(self.space_prjs,rargs.prj)
        tag = work_env.scm().chose_tag(self.space_prjs,rargs.prj,rargs.tag)
        if tag is None:
            raise error.user_break("Sorry, can't checkout empty tag. Please specify a valid tag.")
        rargs.tag = tag
        work_env.scm().checkout(self.space_prjs,rargs.prj,rargs.tag)
        return rg_project(rargs.prj ,self.space_prjs + "/" + rargs.prj + "/_rg/conf.yaml" )
    def tag_release(self,rargs):
        if rargs.tag is None:
            raise error.rigger_exception("Sorry, can't checkout empty tag. Please specify a valid tag.")
        tag = rargs.tag
        work_env.scm().tag_release(self.space_prjs,rargs.prj, tag )

    def chose_project(self):
        prjs = os.listdir(work_env().space_prjs)
        index = 1
        for prj in  prjs:
            print( str(index) + "\t: " + prj)
            index += 1
        print(str(index) +  "\t: Other Project:"  )
        chose_line = get_chose_index("Please Chose Project",index)
        if chose_line is None:
            return  None
        chose = int(chose_line)
        if chose == index:
            other_prj = get_input_line("Please input project")
            return other_prj
        if chose >= 1 and chose <= index :
            return  prjs[chose-1]
        return  None

#    @staticmethod
#    def publish_space():
#        space_root =  env_exp.value("${HOME}/rigger_publish")
#        return space_root

class scm:
    def fetch_project(self,prj):
        pass

class git(scm):
    def __init__(self,repository):
        self.repository = repository
    def fetch_project(self,local,prj,tag=None):
        prjs_root = local
        prj_path  = prjs_root + "/" + prj
        if os.path.exists(prj_path):
            cmd = " cd $PRJS_ROOT/$PRJ; git fetch ;  "
        else:
            cmd = " cd $PRJS_ROOT ; git clone $G$PRJ.git ; cd $PRJ; "
        if not  tag is None:
            cmd += " git checkout $TAG;"
        cmd = Template(cmd).substitute(G=self.repository,PRJ=prj,TAG=tag , PRJS_ROOT=prjs_root )
        print "git cmd:" + cmd;
        code = rg_sh.shexec.execmd(cmd,True)
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
        rg_sh.shexec.execmd(cmd,True)
        last_tags   = open(last_tag_file,'r') .readlines()
        re_tags     = open(re_tag_file,  'r') .readlines()
        rc_tags     = open(rc_tag_file,  'r') .readlines()
        all_tag_file = prjs_root + "/" +  prj + "_*.tags"
        rg_sh.shexec.execmd(Template("rm $TMP").substitute(TMP=all_tag_file))

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
        cmd = Template(cmd).substitute(G=self.repository,PRJ=prj,TAG=tag , PRJS_ROOT=prjs_root )
        rg_sh.shexec.execmd(cmd,True)

    def set_tag(self,ver):
        cmd = "git tag $VER; git push --tags "
        cmd = Template(cmd).substitute(VER=ver)
        rg_sh.shexec.execmd(cmd,True)
    def commit(self,ver,message):
        cmd = """git commit -a -m "$MSG" """
        cimsg = "[ " + ver  + " ]"
        if message is not None:
            cimsg  = cimsg + " " +  message
        cmd = Template(cmd).substitute(MSG=cimsg)
        rg_sh.shexec.execmd(cmd,True,[0,256])
    def push(self):
        cmd="""GIT_POOL=`cat .git/config | grep url | awk '{print $3}' ` ; CUR_BRANCH=`git branch | grep \* | awk '{print $2}'`; git pull $GIT_POOL $CUR_BRANCH ; git push $GIT_POOL $CUR_BRANCH ; """
        rg_sh.shexec.execmd(cmd,True)

    def tag_release(self,local,prj,ori):
        info = "Will tag relase [ r"+ori +  "],Please input  tag message:"
        msg = get_input_line(info)
        cmd = """cd $PRJS_ROOT/$PRJ ;  git tag -a -m "$MSG" r$TAG $TAG ; git push --tags """
        cmd = Template(cmd).substitute(PRJ=prj,PRJS_ROOT=local,TAG=ori,MSG=msg)
        rg_sh.shexec.execmd(cmd,True)

class version:
    first  = 0
    second = 1
    third  = 0
    forth  = 0
    def __init__(self,verfile=None,verstr=None):
        self.verfile = None
        if verfile is not None:
            self.verfile=verfile
            file=open(verfile)
            line=file.readline()
            file.close()
        elif verstr is not None:
            line = verstr
        res=re.match(r"(\d+)\.(\d+)\.(\d+)\.(\d+)",line)
        if not res :
            raise  Exception("bad version format" + line )
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
        if self.verfile is None:
            return
        file=open(self.verfile,'w')
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
        recomTag = False
        needCommit = False
        chose = sys.stdin.read(1)
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

