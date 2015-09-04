import  re , os , string ,  getopt ,sys , unittest,logging
if __name__ == '__main__':
    print(sys.argv[1:] )
    
    pid     = os.getpid()
    lsbtxt  = "/tmp/lsb-%s.txt" %(pid)
    data = os.system("lsb_release -a > %s" %(lsbtxt))  
    file = open(lsbtxt) 
    dist = file.readlines()
    
    print(dist)
