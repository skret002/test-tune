import glob, json, os, re, subprocess, sys, time, requests
from tune_amd import tune
tune_now_pci    = ''
tune_now_series = ''
tune_now_vendor = ''
vendor_ram      = ''
card            = ''


def shutdown_gpus():
    global tune_now_pci, tune_now_series, tune_now_vendor,vendor_ram, card
    with open('/home/test-tune/analytics-card.json', 'r') as f:
        base_settings = json.load(f)

    for i in range(0, len(base_settings)):
        if base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'].isdigit():
            tune_now_pci = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci']
            tune_now_series = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['series']
            tune_now_vendor = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['vendor']
            card = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['card']
    if len(tune_now_pci) == 0 or ':' not in tune_now_pci:
        for i in range(0, len(base_settings)):
            print(base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'], base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci'])
            if base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'] == 'waiting_settings':
                base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'] = 0
                with open('/home/test-tune/analytics-card.json', 'r+') as f:
                    card_settings = json.load(f)
                    for i in range(0, len(card_settings)):
                        if card_settings[i]['card'] == base_settings['card']:
                            card_settings[i] = base_settings
                            f.seek(0)  
                            f.write(json.dumps(card_settings))                                                                                            
                            f.truncate()                 
                tune_now_pci = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci']
                tune_now_series = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['series']
                tune_now_vendor = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['vendor']
                card = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['card']
                break
    if len(tune_now_pci) != 0  and ':'  in tune_now_pci:
        for i in range(0, len(base_settings)): 
            if  base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci'] ==  tune_now_pci:
                pass
            else:
                subprocess.getstatusoutput("timeout  5 sudo echo 1 > /sys/bus/pci/devices/"+str(base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci'])+"/remove")
        tune(tune_now_pci = tune_now_pci,tune_now_series=tune_now_series,tune_now_vendor=tune_now_vendor,vendor_ram=vendor_ram,card=card )        
def distribution():
    pass


if __name__ == '__main__':
    if os.path.exists("/home/test-tune/analytics-card.json") == True and os.path.exists("start-tune") == True:
        shutdown_gpus()