#+*In[11]:*+
#[source, ipython3]
#----
''' 
json-schema for parsed data

{
	"inteval":  <val>,
	"chn": <val>,
	"finfo": <val>,
	"fid":<val>,
    "fname": <name>
	"data": <[]>
	"parsed": 
    [
		[ <byte-no>,
		   [<bits>, <desp>, <val>, <remark>, <val>],
		   [<bits>, <desp>, <val>, <remark>, <val>], 
		],
		[],
        [],
        
        ...
	] 
}


'''

from ebusdataparser import * 
from ibusdataparser import * 


''' frame type '''
FID_FT_INVALID         = 0

FID_FT_BMU_SYSTEM_STATUS        = 0xA0
FID_FT_BMU_SYSTEM_MESSAGE_1     = 0x1A0
FID_FT_BMU_SYSTEM_MESSAGE_2     = 0x2A0
FID_FT_BMU_SYSTEM_MESSAGE_3     = 0x3A0
FID_FT_BMU_INFORMATION_1        = 0x4A0
FID_FT_BMU_INFORMATION_2        = 0x5A0
FID_FT_BMU_INFORMATION_3        = 0x7A0
FID_FT_BMU_STATISTIC_1          = 0x8A0
FID_FT_BMU_STATISTIC_2          = 0x9A0
FID_FT_BMU_VERSION_DATA         = 0xAA0
FID_FT_BMU_CURRENT_INFO         = 0x11A0
FID_FT_BMU_TOTAL_PRESSURE_COLLECTION = 0x14A0

FID_FT_MMU_SYSTEM_STATUS = 0x10000
FID_FT_MMU_INFORMATION_1 = 0x10200
FID_FT_MMU_INFORMATION_2 = 0x10300
FID_FT_MMU_INFORMATION_3 = 0x10400
FID_FT_MMU_CELL_VOL      = 0x20000
FID_FT_MMU_CELL_TEMP     = 0x30000
FID_FT_MMU_VERSION_DATA  = 0xA0000

FID_VS_BMS_CMD_MESSAGE   = 0x4027
FID_BMS_VS_FAULT_MESSAGE = 0xC0EF
FID_BMS_VS_BATT_DATA_MESSAGE_1 = 0xC1EF
FID_BMS_VS_BATT_DATA_MESSAGE_2 = 0xC2EF
FID_BMS_VS_STATUS_MESSAGE_1 = 0xC3EF
FID_BMS_VS_STATUS_MESSAGE_2 = 0xC4EF
FID_BMS_VS_STATUS_MESSAGE_3 = 0xC5EF
FID_BMS_VS_CHARGER_SETPOINT_1 = 0xC6EF
FID_BMS_VS_CHARGER_SETPOINT_2 = 0xC7EF


''' parser list '''
parser_list = [ 
    ( FID_FT_INVALID, None ),  # = 0

    ( FID_FT_BMU_SYSTEM_STATUS,    BMU_System_Status),    #  = 0xA0
    ( FID_FT_BMU_SYSTEM_MESSAGE_1, BMU_System_Message_1), #  = 0x1A0
    ( FID_FT_BMU_SYSTEM_MESSAGE_2, BMU_System_Message_2), #  = 0x2A0
    ( FID_FT_BMU_SYSTEM_MESSAGE_3, BMU_System_Message_3), #  = 0x3A0
    ( FID_FT_BMU_INFORMATION_1,    BMU_Information_1),    #  = 0x4A0
    ( FID_FT_BMU_INFORMATION_2,    BMU_Information_2),    # = 0x5A0
    ( FID_FT_BMU_INFORMATION_3,    BMU_Information_3),    # = 0x7A0
    ( FID_FT_BMU_STATISTIC_1,      BMU_Statistical_Data_1), # = 0x8A0
    ( FID_FT_BMU_STATISTIC_2,      BMU_Statistical_Data_2), # = 0x9A0
    ( FID_FT_BMU_VERSION_DATA,     BMU_Version_Data),    # = 0xAA0
    ( FID_FT_BMU_CURRENT_INFO,     BMU_Current_Information), # = 0x11A0
    ( FID_FT_BMU_TOTAL_PRESSURE_COLLECTION,  BMU_Total_Pressure_Collection), # = 0x14A0

    ( FID_FT_MMU_SYSTEM_STATUS,  MMU_System_Status), #= 0x10000
    ( FID_FT_MMU_INFORMATION_1,  MMU_Information_1), # = 0x10200
    ( FID_FT_MMU_INFORMATION_2,  MMU_Information_2), #  = 0x10300
    ( FID_FT_MMU_INFORMATION_3,  MMU_Information_3), # = 0x10400
    ( FID_FT_MMU_CELL_VOL,       MMU_Cell_Voltage_Data), # = 0x20000
    ( FID_FT_MMU_CELL_TEMP,      MMU_Cell_Temperature_Data), #  = 0x30000
    ( FID_FT_MMU_VERSION_DATA,   MMU_Version_Data), #  = 0xA0000
 
    ( FID_VS_BMS_CMD_MESSAGE  ,  VS2BMS_Command_Message),   #   = 0x4072
    ( FID_BMS_VS_FAULT_MESSAGE,  BMS2VS_Fault_Message),   # = 0xC0EF
    ( FID_BMS_VS_BATT_DATA_MESSAGE_1, BMS2VS_Battery_Data_Message_1 ), # = 0xC1EF
    ( FID_BMS_VS_BATT_DATA_MESSAGE_2, BMS2VS_Battery_Data_Message_2 ), # = 0xC2EF
    ( FID_BMS_VS_STATUS_MESSAGE_1,  BMS2VS_Status_Message_1 ),  # = 0xC3EF
    ( FID_BMS_VS_STATUS_MESSAGE_2,  BMS2VS_Status_Message_2 ),  # = 0xC4EF
    ( FID_BMS_VS_STATUS_MESSAGE_3,  BMS2VS_Status_Message_3 ),  # = 0xC5EF
    ( FID_BMS_VS_CHARGER_SETPOINT_1, BMS2VS_Charger_Setpoint_1 ),  # = 0xC6EF
    ( FID_BMS_VS_CHARGER_SETPOINT_2, BMS2VS_Charger_Setpoint_2 )   #  = 0xC7EF  
]


class BMS_frame:
    def __init__(self, line=None):
            x = line.strip('\n').split(',')
            ''' parse line '''    
            try :
                self.invalid = False
                self.intval = int(x[0], 16) 
                self.chn    = int(x[1], 16)
                self.finfo  = int(x[2], 16)
                self.fid    = int(x[3], 16)
                self.data   = [int(i,16) for i in x[4:]] 
            except :
                print(x)
                raise Exception(str(x))
                return
                 
            ''' parse frame ID '''
            self.fname, self.ft, self.mmu, self.seq = self.parse_fid()  
    
    def print_me(self):
            print("intval: {}".format(self.intval))
            print("chn   : {}".format(self.chn))
            print("finfo : {}".format(hex(self.finfo)))
            print("fid   : {}".format(hex(self.fid)))
            print("data  : {}".format([hex(i) for i in self.data]))

    def print_data(self):
            print([hex(i) for i in self.data])
    
    def dump_to_json(self, parsed=True):
         
        retval = {                 
                 "intval": self.intval,
                 "chn"   : self.chn,
                 "frame info" : self.finfo,
                 "frame id" : self.fid,
                 "ft": self.ft,
                 "name": self.fname,
                 "data"  : self.data,  # ['0x5', '0x0', '0x0', '0x0', '0x3', '0x4', '0x83', '0x1c']
                 }  
        
        
        ext_ft = (FID_VS_BMS_CMD_MESSAGE, #   = 0x4027
                FID_BMS_VS_FAULT_MESSAGE, # = 0xC0EF
                FID_BMS_VS_BATT_DATA_MESSAGE_1, # = 0xC1EF
                FID_BMS_VS_BATT_DATA_MESSAGE_2, # = 0xC2EF
                FID_BMS_VS_STATUS_MESSAGE_1, # = 0xC3EF
                FID_BMS_VS_STATUS_MESSAGE_2, # = 0xC4EF
                FID_BMS_VS_STATUS_MESSAGE_3, # = 0xC5EF
                FID_BMS_VS_CHARGER_SETPOINT_1, # = 0xC6EF
                FID_BMS_VS_CHARGER_SETPOINT_2 ) # = 0xC7EF
               
        mmu_ft = (FID_FT_MMU_SYSTEM_STATUS, # = 0x10000
                FID_FT_MMU_INFORMATION_1, # = 0x10200
                FID_FT_MMU_INFORMATION_2, # = 0x10300
                FID_FT_MMU_INFORMATION_3, # = 0x10400
                FID_FT_MMU_CELL_VOL,      # = 0x20000
                FID_FT_MMU_CELL_TEMP,     # = 0x30000
                FID_FT_MMU_VERSION_DATA)  # = 0xA0000
        
        if self.ft in ext_ft:
            retval["ext"] = 1
         
        if self.ft in mmu_ft:
            retval["mmu"] = 1
        
        if parsed == True:
            retval["remark"] = self.parse_data() 
        
        return retval
    
    def parse_data(self):
        
        ft = self.ft
        
        for i in parser_list:
            if ft==i[0]:
                if i[1]:
                    ac= i[1].__init__.__code__.co_argcount
                    if ac==2:
                        return i[1](data=self.data).parse()
                    if ac==3:
                        # MMU data frame
                        return i[1](mmu=self.mmu, data=self.data).parse()
                    if ac==4:
                        # MMU Cell Vol, Temp data frame
                        return i[1](mmu=self.mmu, seq=self.seq, data=self.data).parse()
                         
        '''
        
        if ft == FID_FT_BMU_SYSTEM_STATUS :
            return BMU_System_Status(data=self.data).parse()
        elif ft == FID_FT_BMU_SYSTEM_MESSAGE_1 :
            return BMU_System_Message_1(data=self.data).parse()
        elif ft == FID_FT_BMU_SYSTEM_MESSAGE_2 :
            return BMU_System_Message_2(data=self.data).parse()
        elif ft == FID_FT_BMU_SYSTEM_MESSAGE_3 :
            return BMU_System_Message_3(data=self.data).parse()
        elif ft == FID_FT_BMU_INFORMATION_1 :
            return BMU_Information_1(data=self.data).parse()
        elif ft == FID_FT_BMU_INFORMATION_2 :
            return BMU_Information_2(data=self.data).parse()
        elif ft == FID_FT_BMU_INFORMATION_3 :
            return BMU_Information_3(data=self.data).parse()
        elif ft == FID_FT_BMU_STATISTIC_1 :
            return BMU_Statistical_Data_1(data=self.data).parse()
        elif ft == FID_FT_BMU_STATISTIC_2 :
            return BMU_Statistical_Data_2(data=self.data).parse()
        elif ft == FID_FT_BMU_VERSION_DATA :
            return BMU_Version_Data(data=self.data).parse()
        elif ft == FID_FT_BMU_CURRENT_INFO :
            return BMU_Current_Information(data=self.data).parse()
        elif ft == FID_FT_BMU_TOTAL_PRESSURE_COLLECTION :
            return BMU_Total_Pressure_Collection(data=self.data).parse()
        
        elif ft == FID_FT_MMU_SYSTEM_STATUS: # = 0x10000
            return MMU_System_Status(data=self.data).parse()
            
        elif ft == FID_FT_MMU_INFORMATION_1: # = 0x10200
            return MMU_Information_1(mmu=self.mmu, data=self.data).parse()
        
        elif ft == FID_FT_MMU_INFORMATION_2: # = 0x10300
            return MMU_Information_2(mmu=self.mmu, data=self.data).parse()
        
        elif ft == FID_FT_MMU_INFORMATION_3: # = 0x10400
            return MMU_Information_3(mmu=self.mmu, data=self.data).parse()
        
        elif ft == FID_FT_MMU_CELL_VOL: #      = 0x20000
            return MMU_Cell_Voltage_Data(mmu=self.mmu, seq=self.seq, data=self.data).parse()
        
        elif ft == FID_FT_MMU_CELL_TEMP: #     = 0x30000
            return MMU_Cell_Temperature_Data(mmu=self.mmu, seq=self.seq, data=self.data).parse()
        
        elif ft == FID_FT_MMU_VERSION_DATA: #  = 0xA0000
             return MMU_Version_Data(mmu=self.mmu, data=self.data).parse()
        else:
            return []
        '''
        
        return []
        
    def parse_fid(self):
        
        fid = self.fid
        
        _mmu = 0xffff
        _seq = 0xffff
        
        if (fid >> 20) ^ 0x18F :
            # print("{} is invalid frame ID!".format(hex(fid)))
            return "Invalid Frame ID", FID_FT_INVALID , _mmu, _seq

        dtype = (fid>>16) & 0xF
        if dtype == 0: #is BMU data 
            # print("fid is BMU data")
            dtype2 = fid &0xFFFF             
            if dtype2 == 0xA0:  # BMU system status 
                return "BMU System Status", FID_FT_BMU_SYSTEM_STATUS, _mmu, _seq

            elif dtype2 == 0x1A0: # BMU system message 1 
                return "BMU System Message 1", FID_FT_BMU_SYSTEM_MESSAGE_1, _mmu, _seq
            
            elif dtype2 == 0x2A0: # BMU system message 2 
                return "BMU System Message 2", FID_FT_BMU_SYSTEM_MESSAGE_2, _mmu, _seq
            
            elif dtype2 == 0x3A0: # BMU system message 3
                return "BMU System Message 3", FID_FT_BMU_SYSTEM_MESSAGE_3, _mmu, _seq

            elif dtype2 == 0x4A0: # BMU information 1
                return "BMU Information 1", FID_FT_BMU_INFORMATION_1, _mmu, _seq
            
            elif dtype2 == 0x5A0: # BMU information 2
                return "BMU Information 2", FID_FT_BMU_INFORMATION_2, _mmu, _seq
            
            elif dtype2 == 0x7A0: # BMU information 3
                return "BMU Information 3", FID_FT_BMU_INFORMATION_3, _mmu, _seq

            elif dtype2 == 0x8A0: # BMU Statistical Data 1  
                return "BMU Statistical Data 1", FID_FT_BMU_STATISTIC_1, _mmu, _seq
            
            elif dtype2 == 0x9A0: # BMU Statistical Data 2 
                return "BMU Statistical Data 2", FID_FT_BMU_STATISTIC_2, _mmu, _seq

            elif dtype2 == 0xAA0: # BMU version data 
                return "BMU Version Data", FID_FT_BMU_VERSION_DATA, _mmu, _seq
                
            elif dtype2 == 0x11A0: # BMU current information  
                # print("BMU current information")
                return "BMU Current Information", FID_FT_BMU_CURRENT_INFO, _mmu, _seq
                
            elif dtype2 == 0x14A0:  
                # print("BMU total pressure collection")
                return "BMU Total Pressure Collection", FID_FT_BMU_TOTAL_PRESSURE_COLLECTION, _mmu, _seq
            # else:
            #    print("invalid fid")

        elif dtype == 1: # is MMU info
            # print("fid is MMU info")
            dtype2 = (fid>>8) & 0xFF
            _mmu = fid & 0xFF
            if dtype2 == 0:
                # print("MMU {} system status".format(mmu))
                return "MMU System Status", FID_FT_MMU_SYSTEM_STATUS, _mmu, _seq
            elif dtype2 == 2:
                # print("MMU {} info 1".format(mmu))
                return "MMU Information 1", FID_FT_MMU_INFORMATION_1, _mmu, _seq
            elif dtype2 == 3:
                #print("MMU {} info 2".format(mmu))
                return "MMU Information 2", FID_FT_MMU_INFORMATION_2, _mmu, _seq                
            elif dtype2 == 4:
                #print("MMU {} info 3".format(mmu))
                return "MMU Information 3", FID_FT_MMU_INFORMATION_3, _mmu, _seq
            #else:
            #    print("invalid fid")

        elif dtype == 2: # is MMU cell voltage 
            # print("fid is MMU cell voltage")
            dtype2 = (fid>>8) & 0xFF
            _mmu = fid & 0xFF
            if dtype2 in range(0,12): # 200~20B
                _seq = dtype2 
                return  "MMU Cell Voltage Data "+str(_seq), FID_FT_MMU_CELL_VOL, _mmu, _seq
            
        elif dtype == 3: # is MMU cell temp. 
            # print("fid is MMU cell temperature")
            dtype2 = (fid>>8) & 0xFF
            _mmu = fid & 0xFF
            if dtype2 <= 0x3:
                _seq = dtype2 
                return  "MMU Cell Temperature Data "+str(_seq), FID_FT_MMU_CELL_TEMP, _mmu, _seq  
        elif dtype == 0xA :
            # print("fid is MMU version or other")
            dtype2 = (fid>>8) & 0xFF
            _mmu = fid & 0xFF
            if  dtype2 == 0:
                # print("MMU Version data fid = {}, data = {}".format(fid, self.data))
                return "MMU Version Data", FID_FT_MMU_VERSION_DATA, _mmu, _seq
         
        elif dtype == 0xF :  # is VS-BMU frame (external CAN BUS
            # print("is vs-bmu")
            dtype2 = fid &0xFFFF             
            if dtype2 == 0x4027: # FID_VS_BMS_CMD_MESSAGE
                return "VS2BMS Command Message", FID_VS_BMS_CMD_MESSAGE, _mmu, _seq
            if dtype2 == 0xC0EF: # FID_BMS_VS_FAULT_MESSAGE
                return "BMS2VS Fault Message", FID_BMS_VS_FAULT_MESSAGE, _mmu, _seq 
            if dtype2 == 0xC1EF: # FID_BMS_VS_BATT_DATA_MESSAGE_1
                return "BMS2VS Battery Data Message 1", FID_BMS_VS_BATT_DATA_MESSAGE_1, _mmu, _seq
            if dtype2 == 0xC2EF: # FID_BMS_VS_BATT_DATA_MESSAGE_2 
                return "BMS2VS Battery Data Message 2", FID_BMS_VS_BATT_DATA_MESSAGE_2, _mmu, _seq
            if dtype2 == 0xC3EF: # FID_BMS_VS_STATUS_MESSAGE_1
                return "BMS2VS Status Message 1", FID_BMS_VS_STATUS_MESSAGE_1, _mmu, _seq
            if dtype2 == 0xC4EF: # FID_BMS_VS_STATUS_MESSAGE_2
                return "BMS2VS Status Message 2", FID_BMS_VS_STATUS_MESSAGE_2, _mmu, _seq
            if dtype2 == 0xC5EF: # FID_BMS_VS_STATUS_MESSAGE_3
                return "BMS2VS Status Message 3", FID_BMS_VS_STATUS_MESSAGE_3, _mmu, _seq
            if dtype2 == 0xC6EF: # FID_BMS_VS_CHARGER_SETPOINT_1
                return "BMS2VS CHarger Set Point 1", FID_BMS_VS_CHARGER_SETPOINT_1, _mmu, _seq
            if dtype2 == 0xC7EF: # FID_BMS_VS_CHARGER_SETPOINT_2
                return "BMS2VS CHarger Set Point 2", FID_BMS_VS_CHARGER_SETPOINT_2, _mmu, _seq
              
        # print("{} is invalid frame ID!".format(hex(fid)))           
        self.invalid = True
        return "Invalid Frame ID", FID_FT_INVALID , _mmu, _seq


#----


#+*In[10]:*+
#[source, ipython3]
#----
if __name__ == "__main__":
    
    ft_list = [
        FID_FT_INVALID ,
        FID_FT_BMU_SYSTEM_STATUS,    #     = 0xA0
        FID_FT_BMU_SYSTEM_MESSAGE_1, #     = 0x1A0
        FID_FT_BMU_SYSTEM_MESSAGE_2, #     = 0x2A0
        FID_FT_BMU_SYSTEM_MESSAGE_3, #     = 0x3A0
        FID_FT_BMU_INFORMATION_1, #        = 0x4A0
        FID_FT_BMU_INFORMATION_2, #        = 0x5A0
        FID_FT_BMU_INFORMATION_3, #        = 0x7A0
        FID_FT_BMU_STATISTIC_1, #          = 0x8A0
        FID_FT_BMU_STATISTIC_2, #          = 0x9A0
        FID_FT_BMU_VERSION_DATA, #         = 0xAA0
        FID_FT_BMU_CURRENT_INFO, #         = 0x11A0
        FID_FT_BMU_TOTAL_PRESSURE_COLLECTION, # = 0x14A0 

       ''' FID_FT_MMU_SYSTEM_STATUS, # = 0x10000
        FID_FT_MMU_INFORMATION_1, # = 0x10200
        FID_FT_MMU_INFORMATION_2, # = 0x10300
        FID_FT_MMU_INFORMATION_3, # = 0x10400
        FID_FT_MMU_CELL_VOL, #      = 0x20000
        FID_FT_MMU_CELL_TEMP, #     = 0x30000
        FID_FT_MMU_VERSION_DATA #  = 0xA0000 
        '''
    ]

    
    
    count = 50000

    with open('../data/00-04.txt', 'r') as f:
        lines = f.readlines()


    # dumper = xlsx_dumper("test4.xlsx")

    # while count > 0:
    for line in lines:    
        if not line:
            break
        try:
            bframe = BMS_frame(line=line)
        except:
            continue
        #if bframe.ft in ft_list :  
        #    print(bframe.dump_to_json())

        #    dumper.dump(ojson=bframe.dump_to_json())

        #count -= 1
        #if count == 0:
        #    break;


    # dumper.save()

#----
