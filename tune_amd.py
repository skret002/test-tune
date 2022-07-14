import glob, json, os, re, subprocess, sys, time, requests


def tune_ellesmere(card, base_settings):
    print(base_settings)





def r(card, tune_now_pci):
    with open('/home/test-tune/analytics-card.json', 'r') as f:
        base_settings = json.load(f)
    for i in range(0, len(base_settings)):
        if  base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['pci'] ==  tune_now_pci and card == base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")]['card']:
            return(base_settings[i][str(base_settings[i].keys()).replace("dict_keys(['","").replace("'])","")])
            
def tune(tune_now_pci,tune_now_series,tune_now_vendor,vendor_ram,card):    
    base_settings = r(card, tune_now_pci)
    if tune_now_series == 'Ellesmere':
        tune_ellesmere(card, base_settings)
    elif tune_now_series == 'Navi':
        pass


if __name__ == '__main__':
    tune()