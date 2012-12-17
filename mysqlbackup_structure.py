import os,sys,time,datetime,shutil
import backup_config
config=backup_config.config
server=config.server
backup_dir=config.backup_dir
user=config.user
pwd=config.pwd
host=config.host
port=config.port
filetime=time.strftime('%Y-%m-%d')
foldername=backup_dir+filetime+"/"
fname=time.strftime('%Y%m%d')
def backup(port,type):
    ## type 1: structure   2 procedures
    global file_size
    try:
        back_dir=foldername+str(port)+"/"
        if ( os.path.exists(foldername)):
            pass
        else:
            os.mkdir(foldername)
        if (os.path.exists(back_dir)):
            pass
        else:
            os.mkdir(back_dir)
        databases_list_cmd="mysql -u %s -p%s -h%s -P%s --silent -N -e 'show databases'" %(user,pwd,host,int(port))
        for database in os.popen(databases_list_cmd).readlines():
            database = database.strip()
            if database == 'information_schema'or database=='performance_schema'or database=='test':
                continue
            else:            
                filename=back_dir+"/"+database+"_"+fname+".str"
                if type==1:
                    dump_sql="mysqldump -u%s -p%s -h %s -e -P%s --opt -d --flush-logs --single-transaction %s >%s" % (user,pwd,host,int(port),database,filename)
                else:
                    dump_sql="mysqldump -u%s -p%s -h %s -e -P%s --opt -R --flush-logs --single-transaction %s >%s" % (user,pwd,host,int(port),database,filename)
                os.popen(dump_sql)
        return 1
    except Exception,ex:
        print ex
def main():
    global port
    if len(sys.argv)<2:
        dump_type=1
    else:
        dump_type=sys.argv[1]
    try:
        if len(port) == 1:
            backup(port[0],dump_type)
        else:       
            for p in port:
                backup(p,dump_type) 
    except Exception,ex:
        print ex
if __name__=="__main__":
    main()
