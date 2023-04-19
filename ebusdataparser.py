'''
vbdataparser.py

Parsers for the external CANBus data frame, VS <--> BMS 

'''

''' VS_BMS_CMD_ Message (ID: 0x18FF4027) '''
class VS2BMS_Command_Message():
    def __init__(self, data):
        self.data = data
    
    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
            
        if data :
            ''' Byte 0 '''
            retbyte = ["0"] # byte 0
            val = data[0]
            if val==1:
                vs_bms_mode_request_desp="Standby Mode"
            elif val==2:
                vs_bms_mode_request_desp="Charge Mode"
            elif val==4:
                vs_bms_mode_request_desp="Discharge Mode"
            else:
                vs_bms_mode_request_desp="Unknown"
                
            retbyte.append(["0-7", "BMS Mode Request", val, vs_bms_mode_request_desp])
                            
            retdata.append(retbyte)
            
            ''' Byte 1 '''
            retbyte = ["1"] # byte 1

            val = data[1] & 1 # bit 0
            retbyte.append(["0", "Disconnect Battery IMD", val, "Disconnect IMD" if val==1 else "Connect IMD"])
    
            val = (data[1]>>1) & 1 # bit 1
            retbyte.append(["1", "Start/Stop Charging Session", val, "Start charging" if val==1 else "Stop charging (1 -> 0)"])

            val = (data[1]>>2) & 1 # bit 2
            retbyte.append(["2", "Bypass Cooling System Request", val, "Bypass Active" if val==1 else "Bypass Inactive"])
    
            retdata.append(retbyte)

            ''' Byte 2 '''
            retbyte = ["2"] # byte 2
            val = data[2]
            retbyte.append(["0-7", "Heart-beat flag", val, ""]) 
                                
            retdata.append(retbyte)
                                
            ''' Byte 3-7 '''
        
        return retdata

''' BMS_VS_FAULT_MESSAGE (ID: 0x18FFC0EF) '''
class BMS2VS_Fault_Message:
    def __init__(self, data=None):
        self.data=data
        
    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            
            ''' byte 0'''
            # BMS Alarm Level 1 Warning 
            retbyte = ["0"] # byte 0
            
            val = data[0] & 1 # bit 0
            retbyte.append(["0", "Cell Voltage Imbalance Warning", val, "Active" if val==1 else "In-active"])
    
            val = (data[0]>>1) & 1 # bit 1
            retbyte.append(["1", "Temperature Imbalance Warning", val, "Active" if val==1 else "In-active"])
            
            val = (data[0]>>2) & 1 # bit 2
            retbyte.append(["2", "Low Insulation Warning", val, "Active" if val==1 else "In-active"])
            
            val = (data[0]>>3) & 1 # bit 3
            retbyte.append(["3", "Cooling System Fault Warning", val, "Active" if val==1 else "In-active"])
            
            retdata.append(retbyte)
                
            ''' byte 1'''
            # BMS Alarm Level 2 Warning
            retbyte = ["1"] # byte 1
            
            val = data[1] & 1 # bit 0
            retbyte.append(["0", "Cell Under-Voltage Level 1", val, "Active" if val==1 else "In-active"])
             
            val = (data[1]>>1) & 1 # bit 1
            retbyte.append(["1", "Cell Over-Voltage Level 1", val, "Active" if val==1 else "In-active"])
    
            val = (data[1] >>2) & 1 # bit 2
            retbyte.append(["2", "Over Temperature Level 1", val, "Active" if val==1 else "In-active"])
    
            val = (data[1] >> 3) & 1 # bit 3
            retbyte.append(["3", "Discharge Over-Current Critical", val, "Active" if val==1 else "In-active"])
    
            val = (data[1] >> 4) & 1 # bit 4
            retbyte.append(["4", "Charge Over-Current Critica", val, "Active" if val==1 else "In-active"])
     
            retdata.append(retbyte) 
            
            ''' byte 2'''
            # BMS Alarm Level 1
            retbyte = ["2"] # byte 2
            
            val = (data[2] >> 1) & 1 # bit 1
            retbyte.append(["1", "Insulation Measurement Device Fault", val, "Active" if val==1 else "In-active"])
     
            retdata.append(retbyte) 
            
            ''' byte 3'''
            # BMS Alarm Level 3 Critical
            retbyte = ["3"] # byte 3
            Byte3_desp = ( "Cell Under-Voltage Level 2", 
                          "Cell Over-Voltage Level 2", 
                          "Over Temperature Level 2", 
                          "Battery System Over Voltage Fault", 
                          "Battery System Under Voltage Fault", 
                          "Cooling System Fault Critical" )
            
            for i in range(len(Byte3_desp)):
                val = (data[3] >> i) & 1 
                retbyte.append([str(i),  Byte3_desp[i], val, "Active" if val==1 else "In-active"])
              
            retdata.append(retbyte)
            
            ''' byte 4'''
            # BMS Alarm Level 4 E-Critical
            retbyte = ["4"] # byte 4
            Byte4_desp = ( "Cell Under-Voltage Level 3", 
                           "Cell Over-Voltage Level 3",
                           "Over Temperature Level 3",
                           "Internal CAN Network Communication Fault",
                           "Middle CAN Network Communication Fault",
                           "Electrical Circuit Breaker fault",
                           "Battery String Relay Adhesion fault",
                           "Cooling System Fault E-Critical" )
            
            for i in range(len(Byte4_desp)):
                val = (data[4] >> i) & 1 
                retbyte.append([str(i),  Byte4_desp[i], val, "Active" if val==1 else "In-active"])
            
            retdata.append(retbyte)
            
            ''' byte 5'''
            retbyte = ["5"] # byte 5
            Byte5_desp = ( "Ultra-High Temperature Fault", 
                          "External CAN Network Communication Fault", 
                          "Low Insulation Fault", 
                          "Pre-charge Failure", 
                          "Battery System Relay Adhesion fault" )
            
            for i in range(len(Byte5_desp)):
                val = (data[5] >> i) & 1 
                retbyte.append([str(i),  Byte5_desp[i], val, "Active" if val==1 else "In-active"])
            
            retdata.append(retbyte)
             
            ''' byte 6'''
            retbyte = ["6"] # byte 6
            Byte6_desp= ( "Battery SOC Low Alarm", 
                         "Battery SOC Too Low Critical", 
                         "Battery SOC Too Low Cut-off", 
                         "Battery System in Limp State", 
                         "Battery System Shutdown Request" )
            
            for i in range(len(Byte6_desp)):
                val = (data[6] >> i) & 1 
                retbyte.append([str(i),  Byte6_desp[i], val, "Active" if val==1 else "In-active"])
            
            retdata.append(retbyte)
            
        return retdata

''' BMS_VS_BATT_DATA_MESSAGE_1 (ID: 0x18FFC1EF) '''
class BMS2VS_Battery_Data_Message_1():
    def __init__(self, data=None):
        self.data=data
        
    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            ''' byte 0-1'''
            retbyte = ["0-1"] # byte 0-1
            val = (data[1]<<8) + data[0]
            retbyte.append(["0-15", "Battery Pack ID", val]) 
            retdata.append(retbyte)
            
            ''' byte 2'''
            retbyte = ["2"] # byte 2
            val = data[2]
            retbyte.append(["0-7", "Designed Battery Capacity", val]) 
            retdata.append(retbyte)
            
            ''' byte 3'''
            retbyte = ["3"] # byte 3
            val = data[3]
            retbyte.append(["0-7", "Current Battery Capacity", val]) 
            retdata.append(retbyte)
            
            ''' byte 4'''
            retbyte = ["4"] # byte 4
            val = data[4]
            retbyte.append(["0-7", "Battery Upper Charge Limit", val]) 
            retdata.append(retbyte)
            
            ''' byte 5'''
            retbyte = ["5"] # byte 5
            val = data[5]
            retbyte.append(["0-7", "Battery SOC Low Limit", val]) 
            retdata.append(retbyte)
            
            ''' byte 6'''
            retbyte = ["6"] # byte 6
            val = data[6]
            retbyte.append(["0-7", "Battery SOC Too Low Limit", val]) 
            retdata.append(retbyte)
            
            ''' byte 7'''
            retbyte = ["7"] # byte 7
            val = data[7]
            retbyte.append(["0-7", "Total Battery Strings", val]) 
            retdata.append(retbyte)

        return retdata

''' BMS_VS_BATT_DATA_MESSAGE_2 (ID: 0x18FFC2EF) '''
class BMS2VS_Battery_Data_Message_2():
    def __init__(self, data=None):
        self.data=data
        
    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            ''' byte 0-3 '''
            retbyte = ["0-3"] # byte 0-3
            val = (data[3]<<24) + (data[2]<<16)+(data[1]<<8) + data[0]
            retbyte.append(["0-31", "Cumulative Battery Energy Counter", val]) 
            retdata.append(retbyte)
            
            ''' byte 4-5 '''
            retbyte = ["4-5"] # byte 4-5
            val = (data[5]<<8) + data[4]
            retbyte.append(["0-15", "Cumulative Charging Counter", val]) 
            retdata.append(retbyte)
            
            ''' byte 6 '''
            retbyte = ["6"] # byte 6
            val = data[6]
            retbyte.append(["0-7", "BMS Software Version - Major Version No.", val]) 
            retdata.append(retbyte)
            
            ''' byte 7 '''
            retbyte = ["7"] # byte 7
            val = data[7]
            retbyte.append(["0-7", "BMS Software Version - Minor Version No.", val]) 
            retdata.append(retbyte)
            
        return retdata

''' BMS_VS_STATUS_MESSAGE_1 (ID: 0x18FFC3EF) '''
class BMS2VS_Status_Message_1():
    def __init__(self, data=None):
        self.data=data
        
    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            ''' byte 0 '''
            retbyte = ["0"] # byte 0
            retbyte.append(["0-7", "Battery System State of Charge(SOC)", data[0]]) 
            retdata.append(retbyte)
            
            ''' byte 1 '''
            retbyte = ["1"] # byte 1
            retbyte.append(["0-7", "Number of Strings Connected", data[1]]) 
            retdata.append(retbyte)
            
            ''' byte 2 '''
            retbyte = ["2"] # byte 2
            val = data[2]
            bms_mode_desp = ("Standby Mode", "Charge Mode", "Discharge Mode", "Unknown") 
            if val in (1,2,4):
                for i in range(3):
                    if (val>>i) == 1:
                        break
            else:
                i = 3
            retbyte.append(["0-7", "BMS Mode", val, bms_mode_desp[i]]) 
            retdata.append(retbyte)
            
            ''' byte 3 '''
            retbyte = ["3"] # byte 3
            val = data[3]
            Batt_sys_status_desp=("Self-Inspection", "Normal Status", "Balance Charging Status", "Limp Status", "Fault Status", "Unknown")
            if val in (1,2,4,8,16):
                for i in range(5):
                    if (val>>i) == 1:
                        break
            else:
                i = 5
            
            retbyte.append(["0-7", "Battery System Status", val, Batt_sys_status_desp[i]]) 
            retdata.append(retbyte)
                
            ''' byte 4-5 '''
            retbyte = ["4-5"] # byte 4-5
            val = (data[5]<<8) + data[4]
            for i in range(16):
                v = (val >> i) & 1
                retbyte.append([str(i), f"String {i} Operation Status", v, "Connected" if v==1 else "Disconnected"]) 
            
            retdata.append(retbyte)
                    
            ''' byte 6 '''
            retbyte = ["6"] # byte 6
            retbyte.append(["0-7", "Battery Insulation Resistance", data[6]]) 
            retdata.append(retbyte)
            
            ''' byte 7 '''
            retbyte = ["7"] # byte 7
            retbyte.append(["0-7", "Heart-beat flag (Toggling 1 and 0)", data[7]]) 
            retdata.append(retbyte) 
          
        return retdata

''' BMS_VS_STATUS_MESSAGE_2 (ID: 0x18FFC4EF) '''
class BMS2VS_Status_Message_2():
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            
            # print("BMS2VS_Status_Message_2 pares")
            
            ''' byte 0-1 '''
            retbyte = ["0-1"] # byte 0-1
            val = (data[1]<<8) + data[0]
            retbyte.append(["0-15", "Battery System Voltage", val]) 
            retdata.append(retbyte)
             
            ''' byte 2-3 '''
            retbyte = ["2-3"] # byte 0-1
            val = (data[3]<<8) + data[2]
            retbyte.append(["0-15", "Battery System Current", val]) 
            retdata.append(retbyte)
            
            ''' byte 4-5 '''
            retbyte = ["4-5"] # byte 4-5
            val = (data[5]<<8) + data[4]
            retbyte.append(["0-15", "Max Discharge Current permitted", val]) 
            retdata.append(retbyte)
            
            ''' byte 6-7 '''
            retbyte = ["6-7"] # byte 6-7
            val = (data[7]<<8) + data[6]
            retbyte.append(["0-15", "Max Regenerative Current permitted", val]) 
            retdata.append(retbyte)
              
        return retdata

''' BMS_VS_STATUS_MESSAGE_3 (ID: 0x18FFC5EF) '''
class BMS2VS_Status_Message_3():
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            ''' byte 0-1 '''
            retbyte = ["0-1"] # byte 0-1
            val = (data[1] <<8) + data[0]
            retbyte.append(["0-15", "Current Maximum Cell Voltage", val]) 
            retdata.append(retbyte)
            
            ''' byte 2-3 '''
            retbyte = ["2-3"] # byte 2-3
            val = (data[3] <<8) + data[2]
            retbyte.append(["0-15", "Current Minimum Cell Voltage", val]) 
            retdata.append(retbyte)
            
            ''' byte 4 '''
            retbyte = ["4"] # byte 4
            val = data[4]
            retbyte.append(["0-7", "Current Maximum Cell Temperature", val]) 
            retdata.append(retbyte)
            
            ''' byte 5 '''
            retbyte = ["5"] # byte 5
            val = data[5]
            retbyte.append(["0-7", "Current Minimum Cell Temperature", val]) 
            retdata.append(retbyte)

        return retdata

''' BMS_VS_CHARGER_SETPOINT_1 (ID: 0x18FFC6EF) '''
class BMS2VS_Charger_Setpoint_1():
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            ''' byte 0-1 '''
            retbyte = ["0-1"] # byte 0-1
            val = (data[1] <<8) + data[0]
            retbyte.append(["0-15", "Maximum Charging Voltage Limit", val]) 
            retdata.append(retbyte)
            
            ''' byte 2-3 '''
            retbyte = ["2-3"] # byte 2-3
            val = (data[3] <<8) + data[2]
            retbyte.append(["0-15", "Maximum Charging Current Limit", val]) 
            retdata.append(retbyte) 
        
        return retdata 
    
''' BMS_VS_CHARGER_SETPOINT_2 (ID: 0x18FFC7EF) '''
class BMS2VS_Charger_Setpoint_2():
    def __init__(self, data=None):
        self.data = data

    def parse(self, data=None):
        retdata = []

        if data is None:
            data = self.data
        
        if data:
            ''' byte 0-1 '''
            retbyte = ["0-1"] # byte 0-1
            val = (data[1] <<8) + data[0]
            retbyte.append(["0-15", "Charging Voltage Set-point", val]) 
            retdata.append(retbyte)
            
            ''' byte 2-3 '''
            retbyte = ["2-3"] # byte 2-3
            val = (data[3] <<8) + data[2]
            retbyte.append(["0-15", "Charging Current Set-point", val]) 
            retdata.append(retbyte) 
        
            ''' byte 4 '''
            retbyte = ["4"] # byte 4
            val = data[4]
            Byte4_desp=("Battery Fault Charging Cut-Off", "General Battery Malfunction", "Battery Temperature Inhibit Charging", "Unknown")
            for i in range(3):
                v = (val >> i) & 1
                retbyte.append([str(i), Byte4_desp[i], v]) 
             
            retdata.append(retbyte)
             
            ''' byte 5 '''
            retbyte = ["5"] # byte 4
            val = data[5] & 1  # BIT 0
            retbyte.append(["0", "BMS IMD Disabled", val]) 
            val = (data[5]>>1) & 1  # BIT 1
            retbyte.append(["1", "BMS Stop Charging", val]) 
             
            retdata.append(retbyte)
            
        return retdata
