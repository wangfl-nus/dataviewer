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

''' BMU System Status '''

sys_run_status_desp = ["Power Up",
					  "Stand By",
					  "Pre-charge",
					  "Ready",
					  "Discarging",
					  "Charging",
					  "Contactors Opening",
					  "Power Off",
					  "","","","","","","",
                       "Error" 
                      ]

sys_run_mode_desp = ["Normal Mode", "Service Mode"] 

failure_level_desp = ["No Trouble", "First Level Failure", "Secondary Level Failure", "Third Level Failure", "", "", "", "", "Prompt Protection"]

'''
input_control_status_b5_desp =[ "Contactor 1 Detection", 
                            "Contactor 2 Detection",
                            "Contactor 3 Detection",
                            "Contactor 4 Detection",
                            "MMU Power State",
                            "High Level Detection, pre-stay",
                            "Low Level Detection Charge Motor Signal",
                            "D14 Low Level Detection, pre-stay" 
                           ]

input_control_status_b6_desp =["Hardware mutual", "VMS KEY Status", "CHG KEY Status", "CC2 Shape State",
                               "","","",""
                              ]

'''
input_control_status_desp=["Contactor 1 Detection", 
                            "Contactor 2 Detection",
                            "Contactor 3 Detection",
                            "Contactor 4 Detection",
                            "MMU Power State",
                            "High Level Detection, pre-stay",
                            "Low Level Detection Charge Motor Signal",
                            "D14 Low Level Detection, pre-stay",
                            "Hardware mutual", "VMS KEY Status", "CHG KEY Status", "CC2 Shape State",
                               "","","","" 
                          ]

output_control_status_desp = [ "Contactor 1 Enable",
                              "Contactor 2 Enable", 
                              "Contactor 3 Enable", 
                              "Contactor 4 Enable", 
                              "Contactor 5 Enable", 
                              "Contactor 6 Enable", 
                              "Contactor 7 Enable", 
                              "MMU Power Enable", 
                              "Low Side Drive Move 1 Enable", 
                              "Low Side Drive Move 2 Enable", 
                              "BMU PWR Lock Make can", 
                              "VCC Make can", 
                              "Sensor PWR ENABLE", 
                              "GPRS PWR ENABLE", 
                              "", ""
                            ]

'''  0x18F000A0, BMU System Status'''
class BMU_System_Status:
    def __init__(self, data=None):
         self.data = data
        
    def parse(self, data=None):
        
        retdata = []

        if data is None:
            data = self.data
            
        if data :
            ''' Byte 1 '''
            retbyte = ["1"] # byte 1
             
            val = data[0] & 0xf  # offset 0, length 4
            retbyte.append(["0-3", "System Running Status", val, sys_run_status_desp[val]])
            
            val = (data[0]>>4) & 0xf  # offset 4, length 4 
            retbyte.append(["4-7", "System Running Mode", val, sys_run_mode_desp[val] if val<3 else ""])
            
            retdata.append(retbyte)
             
            ''' Byte 2 '''
            retbyte = ["2"]  # byte 2 
            
            val = data[1]
            # rmk = "Error Code" # +str(val)
            retbyte.append(["0-7", "Error Code", val])   # , rmk, val           
            retdata.append(retbyte)  
                        
            ''' Byte 3 '''
            retbyte = ["3"]  # byte 3
            val = data[2]& 0x08 
            retbyte.append(["0-7", "Failure Level", val, failure_level_desp[val]])
            retdata.append(retbyte)
            
            ''' Byte 4 '''
            retbyte = ["4"]  # byte 4
            retbyte.append(["0-7", "~", data[3]])
            retdata.append(retbyte)
            
            ''' Byte 5, 6 '''
            retbyte = ["5, 6"]  # byte 5
            
            val =  (data[5]<<8) +  data[4]
            bl = 0x1
            for i in range(12):
                bv = 1 if ((val&bl) > 0) else 0
                rmk = input_control_status_desp[i] # + ": " 
                # rmk += "On" if bv else "Off"  
                retbyte.append([(i%8), "Input Control Status" if i==0 else "", bv, rmk, "On" if bv else "Off"]) 
                bl <<= 1 
             
            retdata.append(retbyte)
            
            #''' Byte 6 ''' 
            # retbyte = ["6"] # byte 6
            
            ##al = data[5] 
            #bl = 0x1       
            #for i in range(4):
            #    bv = 1 if ((val&bl) > 0) else 0
            #    rmk = input_control_status_b6_desp[i] 
            #    retbyte.append([i, "" if i==0 else "", bv, rmk, "On" if bv else "Off"])
            #    bl <<= 1 
             
            #retdata.append(retbyte)
            
            ''' Byte 7 & 8 '''
            retbyte = ["7, 8"]
            
            val = (data[7] << 8) + data[6] 
            bl = 0x1 
            for i in range(14):
                bv = 1 if ((val&bl) > 0) else 0
                rmk = output_control_status_desp[i]  # + ": " 
                # rmk += "On" if bv else "Off"  
                retbyte.append([(i%8), "Output Control Status" if i==0 else "", bv, rmk, "On" if bv else "Off"])
                bl <<= 1 
             
            retdata.append(retbyte)
              
        return retdata
            


''' BMU System Messages '''
 
class BMU_System_Message_1:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1,2", ["0-15", "Battery Insulation Resistance", val, "", round(val,2)]])
            
            ''' byte 3, 4 '''
            val = (data[3] << 8)  + data[2]
            retdata.append(["3,4", ["0-15", "Load Insulation Resistance", val, "", round(val,2)]])
            
            ''' byte 5, 6 '''
            val = (data[5] << 8)  + data[4]
            retdata.append(["5,6", ["0-15", "Total Battery SOH", val, "", round(val*0.1,2)]])  # res = 0.1
            
            ''' byte 7, 8 '''
            val = (data[7] << 8)  + data[6]
            retdata.append(["7,8", ["0-15", "Nominal Battery Capacity", val, "", round(val*0.1,2)]])  # res = 0.1
            
        return retdata


class BMU_System_Message_2:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1,2", ["0-15", "BMU Supply Voltage", round(val*0.1,2), "", val]])  # res 0.1
             
        return retdata

    
class BMU_System_Message_3:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1,2", ["0-15", "Total Battery Voltage", round(val*0.05,2), "", val]])  # res 0.05
            
            ''' byte 3, 4 '''
            val = (data[3] << 8)  + data[2]
            retdata.append(["3,4", ["0-15", "Total Battery Current", round(val*0.05,2), "", val]]) # res 0.05
            
            ''' byte 5, 6 '''
            val = (data[5] << 8)  + data[4]
            retdata.append(["5,6", ["0-15", "Single Cumulative Sum", round(val*0.05,2), "", val]]) # res 0.05
            
            ''' byte 7, 8 '''
            val = (data[7] << 8)  + data[6]
            retdata.append(["7,8", ["0-15", "Total Battey Capacity (SOC)", str(round(val*0.1,2))+"%", "", val]]) # res 0.1
             
        return retdata


''' BMU Information '''

class BMU_Information_1:
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1,2", ["0-15", "Maximum Cell Voltage", round(val*0.001,3), "", val]])  # res 0.001
            
            ''' byte 3    '''
            val =  data[2]
            retdata.append([3, ["0-7", "Highest Monomer Serial Number", val, "", round(val,2)]]) # res 1
            
            ''' byte 4, 5 '''
            val = (data[4] << 8)  + data[3]
            retdata.append(["4,5", ["0-15", "Lowest Cell Voltage", round(val*0.001,3), "", val]])  # res 0.001
            
            ''' byte 6    '''
            val =  data[5]
            retdata.append([6, ["0-7", "Lowest Monomer Serial Number", val, "", round(val,2)]]) # res 1
 
            ''' byte 7, 8 '''
            val = (data[7] << 8)  + data[6]
            retdata.append(["7,8", ["0-15", "Average Cell Voltage", round(val*0.001,3), "", val]])  # res 0.001
            
        return retdata
    

class BMU_Information_2:
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1,2", ["0-15", "Maximum Monomer Temperature", round(val*0.1-40,2), "", val]])  # res 0.1, offset -40
            
            ''' byte 3    '''
            val =  data[2]
            retdata.append(["3", ["0-7", "Maximum Temperature Serial Number", val, "", val]]) # res 1
            
            ''' byte 4, 5 '''
            val = (data[4] << 8)  + data[3]
            retdata.append(["4,5", ["0-15", "Minimum Monomer Temperature", round(val*0.1-40,2), "", val]])  # res 0.1, offset -40
            
            ''' byte 6    '''
            val =  data[5]
            retdata.append(["6", ["0-7", "Minimum Temperature Serial Number", val, "", val]]) # res 1

            ''' byte 7, 8 '''
            val = (data[7] << 8)  + data[6]
            retdata.append(["7,8", ["0-15", "Average Monomer Temperature", round(val*0.1-40,2), "", val]])  # res 0.1, offset -40
            
        return retdata
    

class BMU_Information_3:
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1,2", ["0-15","Cell Voltage Difference", round(val*0.001,3), "", val]])  # res 0.001,
            
            ''' byte 3, 4    '''
            val = (data[3] <<8) + data[2]
            retdata.append(["3,4", ["0-15", "Cell Temperature Difference", round(val*0.1,2), "", val]]) # res 1
            
            ''' byte 5 '''
            retdata.append([5, ["0-7", "~", data[4]]]) 
            
            ''' byte 6    '''
            retdata.append([6, ["0-7", "~", data[5]]]) 

            ''' byte 7, 8 '''
            val = (data[7] << 8)  + data[6]
            retdata.append(["7,8", ["0-15", "The Total Voltage of the load", round(val*0.05,2), "", val]])  # res 0.05
            
        return retdata


''' BMU Statistical Data '''

class BMU_Statistical_Data_1:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1 ~ 4 '''
            val = (data[3] << 24) + (data[2] << 16) + (data[1] << 8) + data[0]
            retdata.append(["1-4", ["0-31", "Charge Accumulation Ampere Hour", round(val*0.1,2), "", val]])  # res 0.1,
                        
            ''' byte 5 ~ 8 '''
            val = (data[7] << 24) + (data[6] << 16) + (data[5] << 8) + data[4]
            retdata.append(["5-8", ["0-31", "Charge Accumulation Watt Hour", round(val*0.1,2), "", val]])  # res 0.1,
            
        return retdata
    

class BMU_Statistical_Data_2:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1 ~ 4 '''
            val = (data[3] << 24) + (data[2] << 16) + (data[1] << 8) + data[0]
            retdata.append(["1-4", ["0-31", "Accumulated Discharge Ampere Hour", round(val*0.1,2), "", val]])  # res 0.1,
                        
            ''' byte 5 ~ 8 '''
            val = (data[7] << 24) + (data[6] << 16) + (data[5] << 8) + data[4]
            retdata.append(["5-8", ["0-31", "Accumulated Discharge Watt Hour", round(val*0.1,2), "", val]])  # res 0.1,
            
        return retdata
    
''' BMU Version Data '''
class BMU_Version_Data:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1 ~ 4'''
            val = (data[3] << 24) + (data[2] << 16) + (data[1] << 8) + data[0]
            retdata.append(["1-4", ["0-31", "BMU Serial Number", val, "", val]])
             
            ''' byte 5 '''
            val = data[4]
            retdata.append(["5", ["0-7", "Software Version Number Section 1", val, "", val]])
            
            ''' byte 6 '''
            val = data[5]
            retdata.append(["6", ["0-7", "Software Version Number Section 2", val, "", val]])
            
            ''' byte 7 '''
            val = data[6]
            retdata.append(["7", ["0-7", "Software Version Number Section 3", val, "", val]])
            
            ''' byte 8 '''
            val = data[7]
            retdata.append(["8", ["0-7", "Software Version Number Section 4", val, "", val]])
             
        return retdata
    
''' BMU Current Information '''
class BMU_Current_Information:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8)  + data[0]
            retdata.append(["1-2", ["0-15", "10s Recharge Current Prediction", round(val*0.05-1600,3), "", val]])  # res 0.05, offset -1600
            
            ''' byte 3, 4    '''
            val = (data[3] <<8) + data[2]
            retdata.append(["3-4", ["0-15", "10s Discharge Current Prediction", round(val*0.05-1600,2), "", val]]) # res 0.05, offset -1600
             
        return retdata
    
''' BMU Total Pressure Collection '''
class BMU_Total_Pressure_Collection:
    def __init__(self, data=None):
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
            
        if data :
            ''' byte 1, 2 '''
            val = (data[1] << 8) + data[0]
            retdata.append(["1,2", ["0-15", "HV1 Voltage", round(val*0.05,2), "", val]])
            
            ''' byte 3, 4 '''
            val = (data[3] << 8) + data[2]
            retdata.append(["3,4", ["0-15", "HV2 Voltage", round(val*0.05,2), "", val]])
            
            ''' byte 5, 6 '''
            val = (data[5] << 8) + data[4]
            retdata.append(["5,6", ["0-15", "Charging Current Requires Evaluation", round(val*0.05-1600,2), "", val, "(Choose fast, slow charging mode and report separately)"]])
                        
            ''' byte 7, 8 '''
            val = (data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", "Charging Voltage Requires Evaluation", round(val*0.05,2), "", val, "(Choose fast, slow charging mode and report separately)"]])
             
        return retdata



''' MMU data '''

class MMU_System_Status:
    def __init__(self, data=None):
        self.data = data
    
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
        
        if data:
            ''' byte 1 '''
            retdata.append(["1", ["0-7", "~", data[0]]])
            
            ''' byte 2 '''
            retdata.append(["2", ["0-7", "~", data[1]]])
            
            ''' byte 3 '''
            retdata.append(["3", ["0-7", "~", data[2]]])
            
            ''' byte 4 '''
            retdata.append(["4", ["0-7", "~", data[3]]])
            
            ''' byte 5 '''
            retdata.append(["5", ["0-7", "~", data[4]]])
            
            ''' byte 6 '''
            retdata.append(["6", ["0-7", "~", data[5]]])
            
            ''' byte 7,8 '''
            val = (data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", "MMU High Pressure Electrical Status", val, "High Voltage Disconnect" if val==0 else ""]])
             
        return retdata
        
class MMU_Information_1:
    def __init__(self, mmu=0, data=None):
        self.mmu = mmu
        self.data = data
         
    def parse(self, mmu=None, data=None):
        
        retdata = []
        
        if mmu is None:
            mmu = self.mmu
        
        if data is None:
            data = self.data
        
        if data and mmu in range(0,32):
            
            rmk = "Module "+str(mmu)
            
            ''' byte 1,2 '''
            val =( data[1] << 8) + data[0] 
            retdata.append(["1,2", ["0-15", "Total Battery voltage (Single Cumulative Sum)", val, round(val*0.05, 2), rmk]])  # res 0.05
            
            ''' byte 3,4 '''
            val =( data[3] << 8) + data[2]
            refined = round(val*0.05-1600, 2)
            retdata.append(["3,4", ["0-15", "Total Battery Current", val, refined, "Charge" if refined >0 else "Discharge", rmk]])  # res 0.05 offset -1600
            
            ''' byte 5,6 '''
            val =( data[5] << 8) + data[4]
            retdata.append(["5,6", ["0-15", "Total Battery SOC", str(round(val*0.1, 2))+"%", val, rmk]])  # res 0.1
                             
            ''' byte 7,8 '''
            val =( data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", "~", val]])
            
        return retdata
     

class MMU_Information_2:
    def __init__(self, mmu=0, data=None):
        self.mmu = mmu
        self.data = data
    
    def parse(self, mmu= None, data=None):
        
        retdata = []
        
        if mmu is None:
            mmu = self.mmu
            
        if data is None:
            data = self.data
        
        if data and mmu in range(0,32):
            
            rmk = "Module "+str(mmu)
            
            ''' byte 1,2 '''
            val = (data[1] << 8) + data[0]
            retdata.append(["1,2", ["0-15", "Maximum Cell Voltage", round(val*0.001, 3), val, rmk]])  # res 0.001
            
            ''' byte 3 '''
            val = data[2]
            retdata.append(["3", ["0-7", "Highest Voltage Serial Number", val, rmk]]) 
            
            ''' byte 4,5 '''
            val = (data[4] << 8) + data[3]
            retdata.append(["4,5", ["0-15", "Lowest Cell Voltage", round(val*0.001, 3), val, rmk]])  # res 0.001
            
            ''' byte 6 '''
            val = data[5]
            retdata.append(["6", ["0-7", "Lowest Voltage Serial Number", val, rmk]])  
            
            ''' byte 7,8 '''
            val = (data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", "Average Cell Voltage", round(val*0.001, 3), val, rmk]])  # res 0.001
              
        return retdata
    

class MMU_Information_3:
    def __init__(self, mmu=0,  data=None):
        self.mmu = mmu
        self.data = data
    
    def parse(self, mmu=None, data=None):
        
        retdata = []
        
        if mmu is None:
            mmu = self.mmu
            
        if data is None:
            data = self.data
        
        if data and mmu in range(0,32):
            
            rmk = "Module "+str(mmu)
            
            ''' byte 1,2 '''
            val = (data[1] << 8) + data[0]
            retdata.append(["1,2", ["0-15", "Maximum Monomer Temperature", round(val*0.1-40, 3), val, rmk]])  # res 0.1  offset -40
            
            ''' byte 3 '''
            val = data[2]
            retdata.append(["3", ["0-7", "Maximum Temperature Serial Number", val, rmk]])
            
            ''' byte 4,5 '''
            val = (data[4] << 8) + data[3]
            retdata.append(["4,5", ["0-15", "Minimum Monomer Temperature", round(val*0.1-40, 3), val, rmk]])  # res 0.1 offset -40
            
            ''' byte 6 '''
            val = data[5]
            retdata.append(["6", ["0-7", "The Lowest Temperature Serial Number", val, rmk]])  
            
            ''' byte 7,8 '''
            val = (data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", "Average Monomer Temperature", round(val*0.1-40, 3), val, rmk]])  # res 0.1 offset -40
             
        return retdata
    

class MMU_Cell_Voltage_Data:
    def __init__(self, mmu = 0, seq =0, data=None, ):
        self.mmu = mmu
        self.seq = seq
        self.data = data
         
    def parse(self, mmu = None, seq = None, data=None):
        
        retdata = []
        
        if mmu is None:
            mmu = self.mmu
        
        if seq is None:
            seq = self.seq
        
        if data is None:
            data = self.data
          
        if data and seq in range(0,12) and mmu in range(0,32):
            
            cell = seq*4+1
            desp = "Cell Voltage "
            rmk = "MMU "+str(mmu)+" Cell "
            
            ''' byte 1,2 '''
            val = (data[1] << 8) + data[0]
            retdata.append(["1,2", ["0-15", desp+str(cell), round(val*0.001, 3), rmk+str(cell), val]])  # res 0.001
            
            ''' byte 3,4 '''
            val = (data[3] << 8) + data[2]
            retdata.append(["3,4", ["0-15", desp+str(cell+1), round(val*0.001, 3), rmk+str(cell+1), val]])  # res 0.001
             
            ''' byte 5,6 '''
            val = (data[5] << 8) + data[4]
            retdata.append(["5,6", ["0-15", desp+str(cell+2), round(val*0.001, 3), rmk+str(cell+2), val]])  # res 0.001
             
            ''' byte 7,8 '''
            val = (data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", desp+str(cell+3), round(val*0.001, 3), rmk+str(cell+3), val]])  # res 0.001
                
        return retdata


class MMU_Cell_Temperature_Data:
    def __init__(self, mmu = 0, seq =0, data=None, ):
        self.mmu = mmu
        self.seq = seq
        self.data = data
         
    def parse(self, mmu = None, seq = None, data=None):
        
        retdata = []
        
        if mmu is None:
            mmu = self.mmu
        
        if seq is None:
            seq = self.seq
        
        if data is None:
            data = self.data
          
        if data and seq in range(0,4) and mmu in range(0,32):
            
            cell = seq*4+1
            desp = "Monomer Temperature "
            rmk = "MMU "+str(mmu)+" Temperature "
            
            ''' byte 1,2 '''
            val = (data[1] << 8) + data[0]
            retdata.append(["1,2", ["0-15", desp+str(cell), round(val*0.1-40, 3), rmk+str(cell), val]])  # res 0.1  offset -40
            
            ''' byte 3,4 '''
            val = (data[3] << 8) + data[2]
            retdata.append(["3,4", ["0-15", desp+str(cell+1), round(val*0.1-40, 3), rmk+str(cell+1), val]])  # res 0.1 offset -40
             
            ''' byte 5,6 '''
            val = (data[5] << 8) + data[4]
            retdata.append(["5,6", ["0-15", desp+str(cell+2), round(val*0.1-40, 3), rmk+str(cell+2), val]])  # res 0.1 offset -40
             
            ''' byte 7,8 '''
            val = (data[7] << 8) + data[6]
            retdata.append(["7,8", ["0-15", desp+str(cell+3), round(val*0.1-40, 3), rmk+str(cell+3), val]])  # res 0.1  offset -40
                
        return retdata


class MMU_Version_Data:
    def __init__(self, mmu=0, data=None):
        self.mmu = mmu
        self.data = data
        
    def parse(self, data=None):
        
        retdata = []
        
        if data is None:
            data = self.data
        
        if data:
            ''' 1~4'''
            val = (data[3]<<24) +(data[2]<<16)+(data[1]<<8)+data[0]
            retdata.append(["1-4", ["0-31", "MMU Numbering", val, "", val]])
            
            ''' 5 '''
            val = data[4]
            retdata.append(["5", ["0-7", "Software Version Number Section 1", val, "", val]])
             
            ''' 6 '''
            val = data[5]
            retdata.append(["6", ["0-7", "Software Version Number Section 2", val, "", val]])
            
            ''' 7 '''
            val = data[6]
            retdata.append(["7", ["0-7", "Software Version Number Section 3", val, "", val]])
            
            ''' 8 '''
            val = data[7]
            retdata.append(["8", ["0-7", "Software Version Number Section 4", val, "", val]])
             
        return retdata
         
