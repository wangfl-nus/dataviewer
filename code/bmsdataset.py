#!/usr/bin/env python
# coding: utf-8

# In[10]:


import json
import importlib

class BMS_Dataset():
    def __init__(self, name='bms-dataset', dataprofile=None):
        self.name = name
        self.dataprofile = dataprofile
        self.ds = [{},{}]  # two channels
        self.ds[0]['bmu']={}
        self.ds[0]['mmus']=[]
        self.ds[1]['bmu']={}
        self.ds[1]['mmus']=[]
        self.rtime = 0 # raltive time 
        self.frames = 0
        self.frame_info = 136  # default value
        self.invalid = False
        
        # validate ds
        if self.dataprofile is not None:
            nch = self.dataprofile.getNrOfChannel()
            chnt = self.dataprofile.getChannelType()
            for i in range(nch):
                if chnt[i] == "CANBUS-EXT-MBMU":
                    del self.ds[i]['bmu']   # delete bmu 
                    del self.ds[i]['mmus']   # delete mmus
                    self.ds[i]['ext']={}
                    self.ds[i]['mbmu'] = self.ds[i]['ext']  # create mbmu referrring to bmu
                    continue
                if chnt[i] == "CANBUS-MBMU-SBMU":
                    self.ds[i]['mbmu'] = self.ds[i]['bmu']  # create mbmu referrring to bmu
                    self.ds[i]['sbmus'] = self.ds[i]['mmus']  # create sbmu referrring to mmus
                    continue
                if chnt[i] == "CANBUS-SBMU-MMU":
                    self.ds[i]['sbmu'] = self.ds[i]['bmu']  # create mbmu referrring to bmu
                    continue 
        
        # self.init_tilte()
        
    #def init_tilte(self):
    #    templates = importlib.import_module('templates') 
    #    
    #    templates.init()
    #    
    #    for i in range(2):  # two channels
    #        self.ds[i]['bmu'] ={k : [] if type(v) is list else v for k, v in templates.bmu_template.items()}  #  templates.bmu_template.copy()
    #        for j in range(6): # six mmus 
    #            self.ds[i]['mmus'].append({k: [] if type(v) is list else v for k,v in templates.mmu_template.items()})
    #    
    #    del templates
        
    def get_title(self, ds, keys=None):
        ret = []
        
        if keys: 
            for _k in keys:
                for i in ds: 
                    if i == "Invalid Frame ID": 
                        continue 
                        
                    for j in ds[i]: 

                        if j == "rtime":
                            continue
 
                        if type(ds[i][j]) is dict:
                            ds1 = ds[i][j]
                            for k in ds1: 
                                if k==_k:    
                                    ret.append(k)
                        else:
                            if j==_k:
                                ret.append(j) 
        else:    
            for i in ds: 
                if i == "Invalid Frame ID": 
                    continue 
                #print(i)
                for j in ds[i]: 

                    if j == "rtime":
                        continue

                    # print("... {}".format(j)) 

                    if type(ds[i][j]) is dict:
                        ds1 = ds[i][j]
                        for k in ds1:
                            # print("... ... {}".format(k))
                            ret.append(k)
                    else:
                        ret.append(j)  
        return ret


    def getValueByColumn(self, chn=0, sheetNo=0, colname=None):
         
        if sheetNo == 0:
            ds = self.ds[chn]['bmu']
        elif sheetNo == 7:
            ds = self.ds[chn]['ext'] 
        else:
            ds = self.ds[chn]['mmus'][sheetNo-1]
            
        for k, v in ds.items():
            for k1,v1 in v.items():
                if type(v1) is dict:
                    for k2, v2 in v1.items():
                        if k2==colname:
                            return v2
                else:
                    if k1==colname:
                            return v1  
        
        return None
    
    def getRichValueByColumn(self, chn=0, sheetNo=0, colname=None):
        
        __cl = self.getValueByColumn(chn=chn, sheetNo=sheetNo, colname=colname)
        
        if colname in ["BMS Mode Request", "BMS Mode"]:
            cl = []
            for i in __cl:
                if i == 1:
                    cl.append("Standby Mode")
                elif i == 2:
                    cl.append("Charge Mode")
                elif i == 4:
                    cl.append("Discharge Mode") 
                 
            return cl, [], [] # [1,2,4], ["Standby Mode", "Charge Mode", "Discharge Mode"]
        
        if colname == "BMS IMD Disabled":
            cl = []
            for i in __cl:
                if i == 0:
                    cl.append("Disconnect IMD")
                else:
                    cl.append("Connect IMD")
            
            return cl, [], [] # [0, 1], ["Disconnect IMD", "Connect IMD"] 
        
        if colname == "Number of Strings Connected":
            cl = []
            for i in __cl:
                cl.append(int(i))
        
            return cl, [*range(0,5,1)], ["0", "1", "2", "3", "4"]
        
        return __cl, [], []
        
    def save(self, fpath='bms-dataset.json'):
        with open(fpath, 'w') as f:
            json.dump(self.ds, f)
   
    def info(self): 
        def __info(df=None, rtime=0):
            if df:
                tlen = 0
                for d in df:
                    v = list(df[d].values())[0]
                    print("{}, ({})".format(d, len(v)))
                    tlen += len(v)
                    for i in df[d]:
                        if type(df[d][i]) is dict:
                            print("\t{})".format(i)) 
                            for j in df[d][i]:
                                print("\t\t{} ({})".format(j, len( df[d][i][j])))
                        else:
                            print("\t{} ({})".format(i, len(df[d][i])))
                            
                print("\ntotal rtime {}".format(rtime))
                print("total length {}".format(tlen))

        # df = self.ds[0]['mmus'][4]
        
        if 'ext' in self.ds[0].keys():
            print("Channel 0 - VS-BMS Data")
            __info(df=self.ds[0]['ext'], rtime=self.rtime)
            
        else:
            print("Channel 0 - BMU Data")
            __info(df=self.ds[0]['bmu'], rtime=self.rtime)

            print("\nChannel 0 - MMU Data") 
            for i in range(len(self.ds[0]['mmus'])):
                print("MMU {}".format(i)) 
                __info(df=self.ds[0]['mmus'][i], rtime=self.rtime)

        if 'ext' in self.ds[1].keys():
            print("Channel 1 - VS-BMS Data")
            __info(df=self.ds[1]['ext'], rtime=self.rtime)
        
        else:
            print("Channel 1 - BMU Data") 
            __info(df=self.ds[1]['bmu'], rtime=self.rtime)

            print("\nChannel 1 - MMU Data") 
            for i in range(len(self.ds[1]['mmus'])):
                print("MMU {}".format(i))
                __info(df=self.ds[1]['mmus'][i], rtime=self.rtime)

    def isvalid(self):
        nch = self.dataprofile.getNrOfChannel()
        if nch != len(self.ds):
            print("error number of channels, profile: {},  ds {}".format(nch, len(self.ds)))
            return False
        
         #for i in range(nch):
            # chninfo = self.dataprofile.getChannelInfo(chn=i)
            # if chninfo['chnt'] == "CANBUS-EXT-MBMU":
                
            
    
    def insert(self, ojson=None):
        if ojson:
            self.rtime += ojson['intval'] # frame.intval
            chn = ojson['chn'] # bframe.chn
            # ojson = bframe.dump_to_json()
            
            if "ext" in ojson.keys(): # is e-canbus 
                if 'ext' in self.ds[chn].keys():
                    self.insert_dataframe(ojson=ojson, df=self.ds[chn]['ext'])
                else:
                    # self.ds[chn]['ext']={}
                    self.invalid = True 
            elif "mmu" in ojson.keys(): # is mmu
                if 'mmus' in self.ds[chn].keys(): 
                    mmu= ojson['frame id'] & 0xff #  bframe.fid & 0xff
                    l = len(self.ds[chn]['mmus'])
                    while(l<=mmu):
                        self.ds[chn]['mmus'].append({})
                        l += 1  
                    self.insert_dataframe(ojson=ojson, df=self.ds[chn]['mmus'][mmu]) 
                else:
                    self.invalid = True
            else :
                # print("is bmu")
                if 'bmu' in self.ds[chn].keys():
                    self.insert_dataframe(ojson=ojson, df=self.ds[chn]['bmu'])
                else:
                    if ojson['name'] != "Invalid Frame ID":  # ignore 'Invalid Frame ID'  
                        self.invalid = True  
                 
    def insert_dataframe(self, ojson=None, df=None):

        if ojson:
            if ojson['name'] not in df.keys():
                df[ojson['name']] = {} 

            self.__handle_line(ojson=ojson, df=df[ojson['name']]) 
            self.frames += 1
             
    def __handle_line(self, ojson=None, df=None):

        if 'rtime' not in df.keys():
            df['rtime']=[]
        df['rtime'].append(self.rtime)

        # handling_inout = False
        remarks = ojson["remark"]
        for byte in remarks:
            # pos = 1
            l = len(byte)
            i = 1
            while i<l:    
                b = byte[i]
                field_name = b[1]

                if field_name == '~':
                    i += 1
                    continue

                if field_name == "Input Control Status": 
                    inout, i = self.__handle_inout(dn=field_name, pos=i, byte=byte)
                    if field_name not in df.keys(): 
                        df[field_name]={} 
                    self.__insert_inout(df[field_name], inout) 
                    continue

                if field_name == "Output Control Status":
                    inout, i = self.__handle_inout(dn=field_name, pos=i, byte=byte)
                    if field_name not in df.keys(): 
                        df[field_name]={} 
                    self.__insert_inout(df[field_name], inout) 
                    continue

                if field_name not in df.keys(): 
                    df[field_name]=[]

                df[field_name].append(b[2])

                i+=1

    def __handle_inout(self, dn, pos, byte):
        # print("handle inout")
        ret = {} 
        i = pos
        for b in byte[pos:]:
            if b[1] in [dn, '']:
                field_name = b[3]
                if field_name not in ret.keys():
                    ret[field_name]=[]
                ret[field_name].append(b[2])
                i += 1
            else:
                break
        return ret, i

    def __insert_inout(self, df, inout):
        for e in inout:
            if e not in df.keys():
                df[e] = []
            df[e].append(inout[e][0])    
            
    
# In[11]:


if __name__ == "__main__":

    import sys
    sys.path.insert(0,'./code')
    from dataparser import *
    from xlsxdumper import *

    files = ['data/00-01.txt', 'data/00-02.txt', 'data/00-03.txt', 'data/00-04.txt', 'data/00-05.txt']

    bms_ds = BMS_Dataset(name="bms-dataset")
    
    for fname in files:
    
        with open(fname, 'r') as f:
            lines = f.readlines()

        for line in lines:    
            if not line:
                break

            try:    
                bms_ds.insert(ojson=BMS_frame(line=line).dump_to_json())
            except Exception as e:
                print(e)
                continue
                
    bms_ds.info() 
    # bms_ds.save('data_test.json')


# In[ ]:




