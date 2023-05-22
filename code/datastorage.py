''' 
 Data Storage 
  
# data storage info 
{
  "ver" :
  "pid" :
  "noc" :
  "proto" :
  "lof": 
  "blkf" : <>  # block table file 
  "datf" : <>  # data file   
}
 
# data block info 
{
"nob": <>  # number of data block
"bt": [    # block table 
	{
	  "sp" : <> # start postion in the file
      "len": <> # length of data block
      "info" : <> # info 
	  "chns": [
		{"sp":<> # start position of the channels
		 "len":  # length of channel data  
		 "nof": <> # number of frames  
		 "du" :
		 "ts" :
		}
		{}  
	  ]  	  
	},   
	{},

]   
}

# data 

'''

from enum import Enum
import datetime, time
import json
import os



''' 
    protocol identifiers
    (to be declared in project property)
'''  
class Comm_Protocol(Enum):
    PSA_EXT_CAN_PROTO = 0
    JKE_INT_CAN_PROTO = 1


'''
    Raw Data
        - representive of raw data
        - APIs to access the physical text-based raw data file  
'''
class RawData:
    def __init__(self, filename=None):
        self.filename = filename
        if self.filename is not None:
            with open(self.filename, 'r') as f:
                self.lines = f.readlines()   # lines
    
    def getRawData(self):
        return self.lines
 
'''
    DataSet
        - A group of data, with start time(date/time) and duration 
        - Subset of the whole data in the data storage
        - Used for data handling and analyzing and visulizing  
'''
class DataSet:
    def __init__(self): 
        self.ds = None

    def getDataSet(self):
        return self.ds    

    
    
DS_VERSION = "0.1"
DEFAULT_PROFILE = {'ver': DS_VERSION, 'pid': 0, 'noc': 2, 'lof':12, 'locked': False }

#
# data storage info
# 
class DataStorage_Info:
    def __init__(self, filename=None):
        self.filename = filename
        if os.path.isfile(self.filename) == True:
            self.__init_from_file()
            self.tosave = False # allow to save only once 
        else:
            self.d = DEFAULT_PROFILE
            self.tosave = True
         
    def setprofile(self, profile={}):
        if self.d['locked'] == True:
            return

        ## TODO: validate the profile

        # merge profiles
        self.d.update(profile)

    def lockprofile(self):
        if self.d['locked'] == False:
            self.d['locked'] = True
            
    def save(self):
        if self.tosave == True:
            with open(self.filename, 'wb') as f:
                f.write(json.dumps(self.d).encode('utf-8'))

    def __init_from_file(self):
        with open(self.filename, 'rb') as f:
            f.seek(0,2)
            len = f.tell()
            f.seek(0,0) 
            b = f.read(len)
            self.d= json.loads(b.decode('utf-8'))


#            
# chnannel            
#
def make_channel(sp, le, nof, du, ts):
    return {"sp":sp, "len": le, "nof":nof, "du":du, "ts":ts}

def timestamp_add(ts, du):
    _dt = datetime.datetime.fromtimestamp(ts) + datetime.timedelta(milliseconds=(du/10)) #
    return time.mktime(_dt.timetuple())

#
# data block info 
#
class DataBlock_Info:
    def __init__(self, filename=None):
        self.filename = filename
        if os.path.isfile(self.filename) == True:
            self.__init_from_file()
        else:
            self.d = {}
            self.d['nob'] = 0
            self.d['blt'] = []
            
    def __init_from_file(self):
        with open(self.filename, 'rb') as f:
            f.seek(0,2)
            len = f.tell()
            f.seek(0,0) 
            b = f.read(len)
            self.d= json.loads(b.decode('utf-8'))
    
    def put(self, bi={}):
        # TODO validate bi
        self.d['nob'] += 1
        self.d['blt'].append(bi)
        
    def get(self, index=0):
        if index < self.d['nob']:
            return self.d['blt'][index]
        else:
            return None
    
    def getLast(self):
        if self.d['nob'] >0:
            return self.d['blt'][self.d['nob']-1]
        else:
            return None
    
    def create(self, chns=[]):
        newb = {}
        length = chns[0]['len'] + chns[1]['len'] 
        if self.d['nob'] > 0:
            lastb = self.d['blt'][self.d['nob'] - 1]
            newb['sp'] = lastb['sp'] + lastb['len']
            newb['len'] = length
            newb['info'] = lastb['info']
        else:
            newb['sp'] = 0
            newb['len'] = length
            newb['info'] = 0 # default info
        newb['chns'] = chns
       
        return newb
      
    def save(self):
        with open(self.filename, 'wb') as f:
            f.write(json.dumps(self.d).encode('utf-8'))

            
#
# Data Storage
#
class DataStorage:
    def __init__(self, filename=None):
        self.filename = filename
        if os.path.isfile(self.filename) == True:
            self.__init_from_file()
        else:
            self.d = {}
            self.d['datastorage-info'] = DataStorage_Info(filename=f'{self.filename}.i')
            self.d['datablock-info'] = DataBlock_Info(filename=f'{self.filename}.bi') 
            self.d['datastorage-info'].d['blkf'] = self.d['datablock-info'].filename # = f'{self.filename}.bi')
            self.d['datastorage-info'].d['dataf'] = f'{self.filename}.dat'
            self.d['data'] = [[],[]]  # two channels
            self.d['cb'] = None # current block 
             
    def setprofile(self, profile={}):
        self.d['datastorage-info'] .setprofile(profile=profile)
    
    def lockprofile(self):
        self.d['datastorage-info'] .lockprofile()
    
    ''' set timestamp'''
    def settimestamp(self, ts=0): 
        if ts==0:
            now = datetime.datetime.now()
            ts =  time.mktime(now.timetuple()) 
         
        for i in range(2):
            #self.dbh.chns[i].ts = ts #  struct.pack("f", ts)
            self.d['cb']['chns'][i]['ts'] = ts
     
    ''' Uplaod raw data to the storage '''    
    def upload(self, rawdata: RawData = None, size=0, ts=0):
        
        if self.d['cb'] is None:
            chns = [] # channels 
            chns.append(make_channel(0, 0, 0, 0, 0))
            chns.append(make_channel(0, 0, 0, 0, 0))
            self.d['cb'] = self.d['datablock-info'].create(chns=chns)
            self.settimestamp(ts=ts)
         
        lines = rawdata.getRawData()
        count = 0
        
        for line in lines:
            x = line.strip('\n').split(',') 
            
            try:
                rs = int(x[0], 16)
                chn = int(x[1], 16)
                finfo  = int(x[2], 16)
                fid    = int(x[3], 16)
                data   = [int(i,16) for i in x[4:]]
            except IndexError:
                print("IndexError: line={}, x={}".format(line, x))
                continue
            except ValueError:
                print("ValueError: line={}, x={}".format(line, x))
                continue

            info = bytearray([rs&0xff]) + bytearray(fid.to_bytes(4, byteorder = 'big')[1:]) 
            data = bytearray([int(i,16) for i in x[4:]]) 
            length = len(info)+len(data)
            if chn in range(2):  # two channels
                self.d['data'][chn].append(info+data)
                self.d['cb']['chns'][chn]['nof'] += 1
                self.d['cb']['chns'][chn]['du'] += rs
                self.d['cb']['chns'][chn]['len'] += length
                # TODO, update chn.du, ds 
                
            if size > 0:
                count += 1
                if count == size:
                    break
        # update sp of channel 1
        self.d['cb']['chns'][1]['sp'] = self.d['cb']['chns'][0]['len']  
        # update data block length
        self.d['cb']['len'] = self.d['cb']['chns'][0]['len'] +  self.d['cb']['chns'][1]['len'] 
        #self.d['datablock-info'].put(self.d['cb'])
          
    def save(self):
        fn = f'{self.filename}.dat'
        with open(fn, 'ab') as f:
            for chn in range(2):
                # ds_pos = f.tell()
                #self.d['cb']['chns']['sp'] = f.tell()
                for d in self.d['data'][chn]:
                    f.write(d) 
                #self.d['cb']['chns']['len'] = f.tell() - self.d['cb']['chns']['sp']
        
        self.d['datablock-info'].put(self.d['cb'])
         
        self.d['datastorage-info'].save() 
        self.d['datablock-info'].save()
        
        # clear current block
        self.d['data'] = [[],[]]  # two channels
        self.d['cb'] = None # current block 
    
    # read data, default du unit 0.1 ms, value is 10 (=1ms)
    def load(self, chn = 0, ts=0, du=10, oft='txt'):
        ds = DataSet()
        
        b_list = [] # temp lcok list
        
        _sts = ts
        _ets = timestamp_add(ts, du)   
        
        _sb = None
        _lb = None
        
        # search in datablock 
        for blk in self.d['datablock-info'].d['blt']:
            _ts1 = blk['chns'][chn]['ts']
            # _ts2 = _ts1 + datetime.timedelta(milliseconds= ( blk['chns'][chn]['du']/10))
            _ts2 = timestamp_add( _ts1, blk['chns'][chn]['du'])
            if _sts >=_ts1 :
                if _sts <= _ts2: 
                    b_list.append(blk)
             
            elif  _ets >= _ts1 :
                b_list.append(blk)
                
        # load data and convert format 
        
        ds = []
        fn = self.d['datastorage-info'].d['dataf']
        lof = self.d['datastorage-info'].d['lof']  # length pf frame (per line in raw data)
        with open(fn, 'rb') as f:
            
            for blk in b_list:
                _sp = blk['sp'] +  blk['chns'][chn]['sp']
                f.seek(_sp, 0)
                buf = f.read(blk['chns'][chn]['len'])
                for i in range(blk['chns'][chn]['nof']):
                    l  = i*lof
                    _bytes = buf[l:l+lof]
                    _ds = []
                    # parse into ds
                    _ds.append(_bytes[0])  # rs
                    _ds.append( int.from_bytes((b'\x18'+_bytes[1:4]), byteorder='big') ) # fid
                    _d = [i for i in _bytes[4:]]
                    _ds.append(_d)
                    ds.append(_ds)       
                    
        return ds  # , b_list ## b_list for test only
