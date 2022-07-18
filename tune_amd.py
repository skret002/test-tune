import glob, json, os, re, subprocess, sys, time, requests

def wr_step_or_data(base_settings):
    with open('/home/test-tune/analytics-card.json', 'r+') as f:
        card_settings = json.load(f)
        for i in range(0, len(card_settings)):
            if card_settings[i]['card'] == base_settings['card']:
                card_settings[i] = base_settings
                f.seek(0)  
                f.write(json.dumps(card_settings))                                                                                            
                f.truncate() 
                break
            
def tune_ellesmere(card, base_settings):
    deadcard = str(base_settings['pci'])+'.dead_gpu'
    if os.path.exists("/home/test-tune/"+deadcard) == False:
        if int(base_settings['status_tune']) == 0:
            pll = int(base_settings['f_power'] + ((base_settings['f_power']/100)*20))
            subprocess.getstatusoutput("echo rocm-smi -d " +str(base_settings['card'])+ " --autorespond Y --setpoweroverdrive "+pll+" --setperflevel manual --setsclk 7 --setmclk 1 --setfan 255 --setslevel 7 1160 980")
            base_settings['status_tune'] = 1
            base_settings['core_freq'] = 1160
            base_settings['core_voltage'] = 0.980
            base_settings['set_pll'] = pll
            wr_step_or_data(base_settings)
        if int(base_settings['status_tune']) == 1:
            while 1 > 0:
                voltage_core = float('{:.4f}'.format(base_settings['core_voltage']-(base_settings['core_voltage']/100)*1))
                subprocess.getstatusoutput("echo atitool -i="+str(base_settings['card'])+" -vddc="+ voltage_core )
                time.sleep(90)
                base_settings['core_voltage'] = voltage_core
                wr_step_or_data(base_settings)
    else:
        step = int(base_settings['status_tune']) + 1          
        base_settings['status_tune'] = step
        wr_step_or_data(base_settings)
        subprocess.getstatusoutput("rm /home/test-tune/"+deadcard)        





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