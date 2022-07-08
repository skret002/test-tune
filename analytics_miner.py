import glob, json, os, re, subprocess, sys, time, requests

MINER  =''
MINER2 =''

hash = []
last_dead={}

teamredminer = '/var/log/miner/teamredminer/teamredminer.log'
def miner_log_json():
    try:
        with open('miner_log.json', 'r+') as f:
            json_data = json.load(f)                                                                                                  
            last_dead['dead_time'] = json_data['dead_time']
    except Exception:
        pass 
def teamredminer_s():
    (status,d)=subprocess.getstatusoutput("tail -n 100 "+teamredminer)
    d = d.split('GPU workers')[-1].split('\n')
    for i in d:
        #print(i[3],i[8],i[-1],i[-2],i[-3]) 0 29.48Mh/s, hw:0 r:0 a:129
        if 'mV' in i and ':' in i and 'C' in i:
            #hash.append({str(i.split("  ")[0][-1]):{'pci':i.split("  ")[1]}}) #'pci':i.split("  ")[1]}
            n = int(i.split("  ")[0][-1])
            hash.append({n:{}})
            hash[n]['pci']=i.split("  ")[1]
        if 'h/s' in i or 'Mh/s' in i and 'hw:' in i and 'GPU' in i:
            i = i.replace('      ',' ').replace('  ',' ').split(' ')
            if i[3].isdigit():
                hash[int(i[3])]['mh'] = i[8].replace('Mh/s','')
                hash[int(i[3])]['hw'] = i[-1].replace('hw:','').split('/')[0].replace('\x1b[0m','')
                hash[int(i[3])]['r'] = i[-2].replace('r:','')
                hash[int(i[3])]['a'] = i[-3].replace('a:','')
                if int(i[-1].replace('hw:','').split('/')[0].replace('\x1b[0m','')) >= round((int(i[-3].replace('a:',''))/100)*3):
                    hash[int(i[3])]['efficiency'] = 'bad'
                else:
                    hash[int(i[3])]['efficiency'] = 'good'
        if 'detected DEAD' in i:
            (status,d)=subprocess.getstatusoutput("touch "+str(i.split(' ')[6].replace('(','').replace(')',''))+'.dead_gpu')
    
    with open('analytics-miner.json', "w+") as file:
        file.seek(0)
        file.write(json.dumps(hash))
        file.truncate()

def reed_log(f_start=0):
    file1 = open("/hive-config/rig.conf", "r")                                                                                                     
    lines = file1.readlines()
    for line in lines:
        if "MINER=" in line:
            MINER = line.replace('MINER=','').replace(' ','').replace('\n','')
        if "MINER2=" in line:
            MINER2 = line.replace('MINER2=','')
    if MINER == 'teamredminer' or MINER2 == 'teamredminer':
        teamredminer_s()
    if f_start==1:
        return(hash)
if __name__ == '__main__':
    reed_log()



