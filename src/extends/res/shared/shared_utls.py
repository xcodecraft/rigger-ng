#coding=utf-8
import os 
def tpldst_path(src,dst) :
    if os.path.isdir(dst) :
        dst   = dst + os.path.basename(src) 
    return dst 
