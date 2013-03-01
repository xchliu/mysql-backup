import os,time,zipfile,datetime,shutil
import sendmail
import backup_config
config=backup_config.config
server=config.server
backup_dir=config.backup_dir
user=config.user
pwd=config.pwd
host=config.host
port=config.port
clear_days=config.clear_days
mailto_list=config.mailto_list
mail_content="Backup_report for "+server+"\n"+"\n"
file_size=0
filetime=time.strftime('%Y-%m-%d')
foldername=backup_dir+filetime+"/"
fname=time.strftime('%Y%m%d')
def backup(port):
    global mail_content,file_size
    try:
        back_dir=foldername+str(port)+"/"
        if ( os.path.exists(foldername)):
            mail_content+="    "+foldername+"   already exists"+"\n"
        else:
            os.mkdir(foldername)
        if (os.path.exists(back_dir)):
            mail_content+="    "+back_dir+"   already exists"+"\n"
        else:
            os.mkdir(back_dir)
        databases_list_cmd="mysql -u %s -p%s -h%s -P%s --silent -N -e 'show databases'" %(user,pwd,host,int(port))
        for database in os.popen(databases_list_cmd).readlines():
            database = database.strip()
            if database == 'information_schema'or database=='performance_schema'or database=='test':
                continue
            else:            
                filename=back_dir+"/"+database+"_"+fname+".sql"
                os.popen("mysqldump -u%s -p%s -h %s -e -P%s --opt --master-data --flush-logs --single-transaction %s >%s" % (user,pwd,host,int(port),database,filename))
                mail_content+="    "+database+":"+str("%.4f"%(float((os.path.getsize(filename)))/float((1024*1024*1024))))+"G"+"\n"               
        return 1
        file_zip(backup_dir+filetime)
    except Exception,ex:
        print ex
       # return ex
       
def file_zip(foldername):
    filename=filetime+".zip"
    f=zipfile.ZipFile(filename,'w',zipfile.ZIP_DEFLATED)
    startdir = foldername
    for dirpath, dirnames, filenames in os.walk(startdir):
        for filename in filenames:
            f.write(os.path.join(dirpath,filename))
    f.close()

def file_clear(): 
    global mail_content  
    clear_file=backup_dir+str(datetime.date.today()-datetime.timedelta(days=clear_days))  
    if (os.path.exists(clear_file)):
        mail_content+="##"+"delete backup file :"+clear_file+"\n"+"\n"
        shutil.rmtree(clear_file)
    else:
        mail_content+="##"+clear_file+"  does not exists!"+"\n"+"\n"
def disk_info():
    global mail_content
    mail_content+="##disk info :"+"\n"
    for line in os.popen("df -lh").readlines():
        mail_content+= line 
       
def main():
    global mail_content,port
    try:
        mail_content+="begin time: "+time.strftime("%Y-%m-%d %H:%M:%S")+"\n" 
        if len(port) == 1:
            backup(port[0])
        else:       
            for p in port:
                backup(p) 
        mail_content+="end time: "+time.strftime("%Y-%m-%d %H:%M:%S")+"\n"
        file_clear()    
        disk_info() 
        sendmail.send_mail(mailto_list, "mysqlbackup report for "+server, mail_content)    
    except Exception,ex:
        print ex
       
if __name__=="__main__":
    main()
