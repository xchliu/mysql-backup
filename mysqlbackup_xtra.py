import os,time,datetime,shutil
import backup_config,sendmail
config=backup_config.config
path_cnf=config.cnf_dir
backup_dir=config.backup_dir
user=config.user
pwd=config.pwd
host=config.host
clear_days=config.clear_days
server=config.server
mailto_list=config.mailto_list
filetime=time.strftime('%Y-%m-%d')
mail_content="Backup_report for "+server+"\n"+"\n"
file_size=0
filetime=time.strftime('%Y-%m-%d')
foldername=backup_dir+filetime+"/"
fname=time.strftime('%Y%m%d')
def backup(backup_type):
    ### backup_type 1:whole  0:incremental
    global mail_content,file_size
    try:
        if backup_type==1:
            back_dir=foldername+"back_basic"
        else:
            back_dir=foldername+"back_incr"+time.strftime('%H')        
        if ( os.path.exists(foldername)):
            mail_content+="    "+foldername+"   already exists"+"\n"
        else:
            os.mkdir(foldername)      
        if backup_type==1:
            backup_cmd=" innobackupex --user=%s --password=%s --host=%s --defaults-file=%s %s --no-timestamp" % (user,pwd,host,path_cnf,back_dir)
        elif backup_type==0:
            if time.strftime('%H')=="01":
                base_dir=foldername+"back_basic"+"/"
            else:
                base_dir=foldername+"back_incr"+str((datetime.datetime.now() - datetime.timedelta(hours=1)).hour)         
            backup_cmd=" innobackupex --incremental --incremental-basedir=%s --user=%s --password=%s --host=%s --defaults-file=%s %s --no-timestamp" % (base_dir,user,pwd,host,path_cnf,back_dir)           
        os.popen(backup_cmd)
        #file_zip(backup_dir+filetime)
    except Exception,ex:
        return ex
def file_clear():    
    global mail_content  
    clear_file=backup_dir+str(datetime.date.today()-datetime.timedelta(days=clear_days))    
    if (os.path.exists(clear_file)):
        shutil.rmtree(clear_file)
        mail_content+="delete files : "+clear_file
    else:
        mail_content+=clear_file+"  does not exists!"
def main():
    global mail_content
    try:
        if time.strftime('%H')=="00":
            back_type=1
        else:
            back_type=0
        mail_content+="begin time: "+time.strftime("%Y-%m-%d %H:%M:%S")+"\n" 
        backup(back_type) 
        mail_content+="end time: "+time.strftime("%Y-%m-%d %H:%M:%S")+"\n"
        file_clear() 
        #print mail_content
        #disk_info() 
        sendmail.send_mail(mailto_list, "mysqlbackup report for "+server, mail_content)    
    except Exception,ex:
        print ex   
if __name__=="__main__":
    main()