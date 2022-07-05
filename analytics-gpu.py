import glob, json, os, re, subprocess, sys, time, requests

init_data = []

def navi_and_up(nc, num):
    global init_data
    (status,dpm_str)=subprocess.getstatusoutput("upp -p /sys/class/drm/card"+ num +"/device/pp_table get smc_pptable/FreqTableGfx")
    dpm_str = dpm_str.replace('ERROR: Decoded data does not contain any value, you probably wanna look deeper into data;', '').replace('\nERROR: Incorrect variable path: smc_pptable/FreqTableGfx','').replace(' ','').split(',')
    init_data[nc][num]['FreqTableGfx_dpm_min'] = int(dpm_str[0])
    init_data[nc][num]['FreqTableGfx_dpm_max'] = int(dpm_str[-1])
    (status,FreqGfx)=subprocess.getstatusoutput("upp -p /sys/class/drm/card"+ num +"/device/pp_table get smc_pptable/FreqTableFreqTableGfx"+ str(dpm_str[-1]))
    init_data[nc][num]['FreqTableGfx'] = int(FreqGfx)
    (status,dpm_str)=subprocess.getstatusoutput("upp -p /sys/class/drm/card"+ num +"/device/pp_table get smc_pptable/FreqTableUclk")
    dpm_str = dpm_str.replace('ERROR: Decoded data does not contain any value, you probably wanna look deeper into data;', '').replace('\nERROR: Incorrect variable path: smc_pptable/FreqTableGfx','').replace(' ','').split(',')
    init_data[nc][num]['FreqTableUclk_dpm_min'] = int(dpm_str[1])
    init_data[nc][num]['FreqTableUclk_dpm_max'] = int(dpm_str[-1])
    (status,FreqTableUclk)=subprocess.getstatusoutput("upp -p /sys/class/drm/card"+ num +"/device/pp_table get smc_pptable/FreqTableFreqTableGfx"+ str(dpm_str[-1]))
    init_data[nc][num]['FreqTableUclk'] = int(FreqTableUclk)
    (status,core_voltege)=subprocess.getstatusoutput("upp -p /sys/class/drm/card"+ num +"/device/pp_table get smc_pptable/MinVoltageUlvGfx smc_pptable/MaxVoltageGfx")
    init_data[nc][num]['core_voltege_min'] = int(core_voltege.split("\n")[0])
    init_data[nc][num]['core_voltege_max'] = int(core_voltege.split("\n")[1])
    (status,dpm_str)=subprocess.getstatusoutput("upp -p /sys/class/drm/card3/device/pp_table get smc_pptable/MemMvddVoltage")
    dpm_str = dpm_str.replace('ERROR: Decoded data does not contain any value, you probably wanna look deeper into data;', '').replace('\nERROR: Incorrect variable path: smc_pptable/FreqTableGfx','').replace(' ','').split(',')
    init_data[nc][num]['MemMvddVoltage_dpm_min'] = int(dpm_str[1])
    init_data[nc][num]['MemMvddVoltage_dpm_max'] = int(dpm_str[-1])     
    (status,MemMvddVoltage)=subprocess.getstatusoutput("upp -p /sys/class/drm/card"+ num +"/device/pp_table get smc_pptable/MemMvddVoltage"+ str(dpm_str[-1]))   
    init_data[nc][num]['MemMvddVoltage'] = int(MemMvddVoltage)    

def ellesmere(nc, num):
    global init_data
    (status,str_data)=subprocess.getstatusoutput("cat /sys/class/drm/card"+ num +"/device/pp_od_clk_voltage")
    buf = " ".join(str_data.split("\nOD_")[0].split())
    buf = buf.split(':')[-1].split(' ')
    init_data[nc][num]['core_freq'] = int(buf[1].replace('MHz',''))
    init_data[nc][num]['core_voltage'] = int(buf[2].replace('mV',''))
    buf = " ".join(str_data.split("\nOD_")[1].split())
    buf = buf.split(':')[-1].split(' ')
    init_data[nc][num]['mem_freq'] = int(buf[1].replace('MHz',''))
    init_data[nc][num]['mem_voltage'] = int(buf[2].replace('mV',''))
    
def amd_f_data():
    global init_data
    card_num=[]
    series = ''
    (status,output)=subprocess.getstatusoutput("rocm-smi")
    for i in output.split('\n'):
        if i.split(" ")[0].isdigit():
            card_num.append(i.split(" ")[0])
    nc = 0
    for num in card_num:
        num=str(num)
        init_data.append({str(num):{"card":num}})
        (status,output)=subprocess.getstatusoutput("rocm-smi -d " + num + " -a")
        for i in output.split('\n'):
            if 'PCI Bus:' in i:
                init_data[nc][num]["pci"] = i.split(" ")[-1]
            if 'Average Graphics Package Power (W)' in i:
                try:
                    init_data[nc][num]['f_power'] = int(i.split(" ")[-1])
                except Exception:
                    init_data[nc][num]['f_power'] = int(float(i.split(" ")[-1]))
            if 'series' in i:
                name_str = " ".join(i.split())
                name = name_str.split(':')[-1]
                init_data[nc][num]['name'] = name
            if 'Navi' in i:
                init_data[nc][num]['series'] = 'Navi'
                navi_and_up(nc, num)
            if 'Ellesmere' in i:
                init_data[nc][num]['series'] = 'Ellesmere'
                ellesmere(nc, num)
        nc=nc+1       
    with open('analytics-card.json', "w+") as file:
        file.seek(0)
        file.write(json.dumps(init_data))
        file.truncate()
        
if __name__ == '__main__':
    amd_f_data()