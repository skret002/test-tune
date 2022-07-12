from ast import main
import glob, json, os, re, subprocess, sys, time, requests
from unicodedata import name

tune_now_pci    = ''
tune_now_series = ''
tune_now_vendor = ''
vendor_ram      = ''
def shutdown_gpus():
    with open('analytics-card.json', 'r') as f:
        base_settings = json.load(f)
    for i in range(0, len(base_settings)):
        if base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'].isdigit():
            tune_now_pci = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci']
            tune_now_series = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['series']
            tune_now_vendor = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['vendor']
    if len(tune_now_pci) == 0 or ':' not in tune_now_pci:
        for i in range(0, len(base_settings)):
            if base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'] == 'waiting_settings':
                base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['status_tune'] = 0
                tune_now_pci = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci']
                tune_now_series = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['series']
                tune_now_vendor = base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['vendor']
                break
    if len(tune_now_pci) != 0 and ':'  in tune_now_pci:
        for i in range(0, len(base_settings)): 
            if  tune_now_pci == base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci'] ==  tune_now_pci:
                pass
            else:
                subprocess.getstatusoutput("timeout  5 sudo echo 1 > /sys/bus/pci/devices/"+str(tune_now_pci)+"/remove") 
def distribution():
    pass


if __name__ == '__main__':
    if os.path.exists("analytics-card.json") == True and os.path.exists("start-tune") == True:
        shutdown_gpus()