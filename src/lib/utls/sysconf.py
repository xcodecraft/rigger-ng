#coding=utf-8
import datetime , shutil ,os ,getopt, sys
import string   , logging ,re
import setting ,interface
from string import Template
# from utls.pattern import end_keeper
from rg_io import *

class sysconf:
    def __init__(self,filename,commenttag="#"):
        self.conffile=filename 
        self.commenttag=commenttag
    def write_conf(self,nfile,content,isclean=False):
        if isclean : 
            return 
        nfile.write(self.beg )
        nfile.write(self.timetag)
        if isinstance(content,list) :
            for line in content :
                nfile.write(line)
        else:
            nfile.write(content + "\n")
        nfile.write(self.end )
    def clean(self,key):
        return self.replace(key,"",isclean=True)

    def replace(self,key,content,isclean=False):
        begtpl="$TAG $KEY,POWER BY RIGGER-NG---BEGIN\n"
        endtpl="$TAG $KEY,POWER BY RIGGER-NG---END\n"
        datetpl="$TAG DATE: $DATE\n"

        now    = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M")
        name   = os.path.basename(self.conffile)
        backup = "/tmp/" +  name + "_" +  now
        shutil.copy(self.conffile,backup)
        self.beg     = Template(begtpl).substitute(TAG=self.commenttag,KEY=key)
        self.end     = Template(endtpl).substitute(TAG=self.commenttag,KEY=key)
        self.timetag = Template(datetpl).substitute(TAG=self.commenttag,DATE=now)
        newcron      = self.conffile + ".new"
        file         = open(self.conffile)
        nfile        = open(newcron ,"w")
        ispass     = False
        have_write = False
        for  line in file:
            if line == self.beg :
                ispass = True
            if not ispass :
                nfile.write(line)
            if line == self.end :
                ispass     = False
                have_write = True
                self.write_conf(nfile,content,isclean)
        if not have_write  : 
            self.write_conf(nfile,content,isclean)
        nfile.close()
        file.close()
        return newcron
        # shutil.copy(newfileName ,self.conffile)

    def replace_by_file(self,key,contentFile):
        file    = open(contentFile)
        content = file.readlines()
        newcron = self.replace(key,content)
        file.close()
        return newcron 

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "f:n:c:t:p:", ["conf=","name=","content=","tag=","type="])
    tag="#"
    type="string"
    content=""
    file=None
    name="unknow"
    for o, a in opts:
        if o == "-t":
            tag= a  
        if o == "-c":
            content=a
        if o == "-f":
            file=a
        if o == "-n":
            name=a
        if o == "-p":
            type=a

    if file != None :
        conf = sysconf(file,tag)
        if type == "file":
            conf.replace_by_file(name,content)
        else:
            conf.replace(name,content)
        print( Template(" update  conf [$FILE] over!").substitute(FILE=file))
    else:
        print("None file")
