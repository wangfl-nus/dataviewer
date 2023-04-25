
''' BMS Data Set json schema 

"frame info":136,

[
# channel 0
{

'bmu': {
  "log":{},  # any comments for analysis
  "BMU System Status": 
  {
    "rtime":[], # relative time, unit 0.1ms
    "System Running Status":[],
    "System Running Mode":[],
    "Error Code":[],
    "Failure Level":[],
    "Input Control Status":{ 
        "Contactor 1 Detection":[],
        "Contactor 2 Detection":[],
        "Contactor 3 Detection":[],
        "Contactor 4 Detection":[],
        "MMU Power State":[],
        "High Level Detection, pre-stay":[],
        "Low Level Detection Charge Motor Signal":[],
        "D14 Low Level Detection, pre-stay":[],
        "Hardware mutual":[],
        "VMS KEY Status":[],
        "CHG KEY Status":[],
        "CC2 Shape State":[],
      },
     "Output Control Status":{
        "Contactor 1 Enable":[],
        "Contactor 2 Enable":[],
        "Contactor 3 Enable":[],
        "Contactor 4 Enable":[],
        "Contactor 5 Enable":[],
        "Contactor 6 Enable":[],
        "Contactor 7 Enable":[],
        "MMU Power Enable":[],
        "Low Side Drive Move 1 Enable":[],
        "Low Side Drive Move 2 Enable":[],
        "BMU PWR Lock Make can":[],
        "VCC Make can":[],
        "Sensor PWR ENABLE":[],
        "GPRS PWR ENABLE":[]
      } 
    
  },
  

}

'mmus': [
    
    # mmu0
    {} 
    
    # mmu1 
    {} 
] 
,


# channel 1

{}
]




'''

# tempalate for ds["ext']
ext_template = {
    "VS2BMS Command Message": {
        "BMS Mode Request": [],
        "Disconnect Battery IMD": [], 
        "Start/Stop Charging Session": [],
        "Bypass Cooling System Request": [],
        "Heart-beat flag": [] 
    },
    
    "BMS2VS Fault Message": {
        "Cell Voltage Imbalance Warning": [],
        "Temperature Imbalance Warning": [],
        "Low Insulation Warning": [],
        "Cooling System Fault Warning":[],
        
        "Cell Under-Voltage Level 1": [],
        "Cell Over-Voltage Level 1": [],
        "Over Temperature Level 1": [],
        "Discharge Over-Current Critical": [],
        "Charge Over-Current Critica": [], 
        
        "Insulation Measurement Device Fault": [],
        
        "Cell Under-Voltage Level 2": [],
        "Cell Over-Voltage Level 2": [], 
        "Over Temperature Level 2": [], 
        "Battery System Over Voltage Fault": [],
        "Battery System Under Voltage Fault": [],
        "Cooling System Fault Critical": [],
        
        "Cell Under-Voltage Level 3": [],
        "Cell Over-Voltage Level 3": [], 
        "Over Temperature Level 3": [], 
        "Internal CAN Network Communication Fault": [],
        "Middle CAN Network Communication Fault": [], 
        "Electrical Circuit Breaker fault": [],
        "Battery String Relay Adhesion fault": [],
        "Cooling System Fault E-Critical": [], 
        
        "Ultra-High Temperature Fault": [], 
        "External CAN Network Communication Fault": [],
        "Low Insulation Fault" : [],
        "Pre-charge Failure": [], 
        "Battery System Relay Adhesion fault": [],
        
        "Battery SOC Low Alarm": [],
        "Battery SOC Too Low Critical": [], 
        "Battery SOC Too Low Cut-off": [], 
        "Battery System in Limp State": [],
        "Battery System Shutdown Request": []
    },
    
    "BMS2VS Battery Data Message 1": {
        "Battery Pack ID": [], 
        "Designed Battery Capacity": [],
        "Current Battery Capacity": [], 
        "Battery Upper Charge Limit": [], 
        "Battery SOC Low Limit": [], 
        "Battery SOC Too Low Limit": [], 
        "Total Battery Strings": []
    },
    
    "BMS2VS Battery Data Message 2": {
        "Cumulative Battery Energy Counter": [],
        "Cumulative Charging Counter": [],
        "BMS Software Version - Major Version No.": [],
        "BMS Software Version - Minor Version No.": []  
    },
    
    "BMS2VS Status Message 1": {
        "Battery System State of Charge(SOC)": [],
        "Number of Strings Connected": [], 
        "BMS Mode": [],
        "Battery System Status": [],
        "String 0 Operation Status": [],
        "String 1 Operation Status": [],
        "String 2 Operation Status": [],
        "String 3 Operation Status": [],
        "String 4 Operation Status": [],
        "String 5 Operation Status": [],
        "String 6 Operation Status": [],
        "String 7 Operation Status": [],
        "String 8 Operation Status": [],
        "String 9 Operation Status": [],
        "String 10 Operation Status": [],
        "String 11 Operation Status": [],
        "String 12 Operation Status": [], 
        "String 13 Operation Status": [],
        "String 14 Operation Status": [],
        "String 15 Operation Status": [], 
        "Battery Insulation Resistance": [],
        "Heart-beat flag (Toggling 1 and 0)": [] 
    },
    
    "BMS2VS Status Message 2": {
        "Battery System Voltage": [],
        "Battery System Current": [],
        "Max Discharge Current permitted": [],
        "Max Regenerative Current permitted": []
    },
    
    "BMS2VS Status Message 3": {
        "Current Maximum Cell Voltage": [],
        "Current Minimum Cell Voltage": [], 
        "Current Maximum Cell Temperature": [],
        "Current Minimum Cell Temperature": []
    },
    
    "BMS2VS CHarger Set Point 1": {
        "Maximum Charging Voltage Limit": [],
        "Maximum Charging Current Limit": []
    },
    
    "BMS2VS CHarger Set Point 2": {
        "Charging Voltage Set-point": [],
        "Charging Current Set-point": [],
        "Battery Fault Charging Cut-Off": [],
        "General Battery Malfunction": [],
        "Battery Temperature Inhibit Charging": [],
        "BMS IMD Disabled": [],
        "BMS Stop Charging": []   
    }
}

# tempalate for ds["bmu']
bmu_template = {
    "BMU System Status": { 
        "System Running Status":[], 
        "System Running Mode":[], 
        "Error Code":[],	
        "Failure Level":[],	
        "Input Control Status":{
            "Contactor 1 Detection":[],
            "Contactor 2 Detection":[],
            "Contactor 3 Detection":[],
            "Contactor 4 Detection":[],
            "MMU Power State":[],
            "High Level Detection, pre-stay":[],
            "Low Level Detection Charge Motor Signal":[],
            "D14 Low Level Detection, pre-stay":[],
            "Hardware mutual":[],
            "VMS KEY Status":[],
            "CHG KEY Status":[],
            "CC2 Shape State":[] 
        },
        "Output Control Status":{
            "Contactor 1 Enable":[],
            "Contactor 2 Enable":[],
            "Contactor 3 Enable":[],
            "Contactor 4 Enable":[],
            "Contactor 5 Enable":[],
            "Contactor 6 Enable":[],
            "Contactor 7 Enable":[],
            "MMU Power Enable":[],
            "Low Side Drive Move 1 Enable":[],
            "Low Side Drive Move 2 Enable":[],
            "BMU PWR Lock Make can":[],
            "VCC Make can":[],
            "Sensor PWR ENABLE":[],
            "GPRS PWR ENABLE":[]
        }
    },
    
    "BMU System Message 1": { 
        "Battery Insulation Resistance":[],	
        "Load Insulation Resistance":[],
        "Total Battery SOH":[],
        "Nominal Battery Capacity":[]
    },
    
    "BMU System Message 2": {
        "BMU Supply Voltage":[]
    },
    
    "BMU System Message 3": {
        "Total Battery Voltage":[],
        "Total Battery Current":[],
        "Single Cumulative Sum":[],
        "Total Battey Capacity (SOC)":[]
    },
    
    "BMU Information 1": {
        "Maximum Cell Voltage":[],	
        "Highest Monomer Serial Number":[],
        "Lowest Cell Voltage":[],
        "Lowest Monomer Serial Number":[],
        "Average Cell Voltage":[]
    },
    
    "BMU Information 2": { 
        "Maximum Monomer Temperature":[],	
        "Maximum Temperature Serial Number":[],
        "Minimum Monomer Temperature":[],
        "Minimum Temperature Serial Number":[],
        "Average Monomer Temperature":[]
    },
    
    "BMU Information 3": { 
        "Cell Voltage Difference":[],	
        "Cell Temperature Difference":[],	
        "The Total Voltage of the load":[]
    },
    
    "BMU Statistical Data 1": {
        "Charge Accumulation Ampere Hour":[],	
        "Charge Accumulation Watt Hour":[]
    },
    
    "BMU Statistical Data 2": { 
        "Accumulated Discharge Ampere Hour":[],	
        "Accumulated Discharge Watt Hour":[]
    },
    
    "BMU Version Data": { 
        "BMU Serial Number":[],	
        "Software Version Number Section 1":[],	
        "Software Version Number Section 2":[],	
        "Software Version Number Section 3":[],
        "Software Version Number Section 4":[]
    },
    
    "BMU Current Information": { 
        "10s Recharge Current Prediction":[],	
        "10s Discharge Current Prediction":[]
    },
    
    "BMU Total Pressure Collection": { 
        "HV1 Voltage":[],	
        "HV2 Voltage":[],	
        "Charging Current Requires Evaluation":[],	
        "Charging Voltage Requires Evaluation":[]
    } 
}

# template for ds['mmus'][]
mmu_template = {
    "MMU System Status": {"MMU High Pressure Electrical Status":[]},
    
    "MMU Information 1":{
        "Total Battery voltage (Single Cumulative Sum)":[],
        "Total Battery Current":[],
        "Total Battery SOC":[]
    },
    
    "MMU Information 2": { 
        "Maximum Cell Voltage":[],
        "Highest Voltage Serial Number":[],
        "Lowest Cell Voltage":[],
        "Lowest Voltage Serial Number":[],
        "Average Cell Voltage":[]
    },
    
    "MMU Information 3": { 
        "Maximum Monomer Temperature":[],
        "Maximum Temperature Serial Number":[],
        "Minimum Monomer Temperature":[],
        "The Lowest Temperature Serial Number":[],
        "Average Monomer Temperature":[]
    },
    
    "MMU Version Data": {
        "MMU Numbering":[],
        "Software Version Number Section 1":[],
        "Software Version Number Section 2":[],
        "Software Version Number Section 3":[],
        "Software Version Number Section 4":[]
    },
    
    "MMU Cell Voltage Data 1": {
        "Cell Voltage 1":[],	
        "Cell Voltage 2":[],
        "Cell Voltage 3":[],
        "Cell Voltage 4":[]
    },
    
    "MMU Cell Voltage Data 2": {
        "Cell Voltage 5":[],	
        "Cell Voltage 6":[],
        "Cell Voltage 7":[],
        "Cell Voltage 8":[]
    },
    
    "MMU Cell Voltage Data 3": {
        "Cell Voltage 9":[],	
        "Cell Voltage 10":[],
        "Cell Voltage 11":[],
        "Cell Voltage 12":[]
    }, 
    
    "MMU Cell Voltage Data 4": {
        "Cell Voltage 13":[],	
        "Cell Voltage 14":[],
        "Cell Voltage 15":[],
        "Cell Voltage 16":[]
    },
    
    "MMU Cell Voltage Data 5": {
        "Cell Voltage 17":[],	
        "Cell Voltage 18":[],
        "Cell Voltage 19":[],
        "Cell Voltage 20":[]
    },
    
    "MMU Cell Voltage Data 6": {
        "Cell Voltage 21":[],	
        "Cell Voltage 22":[],
        "Cell Voltage 23":[],
        "Cell Voltage 24":[]
    },  
    
    "MMU Cell Voltage Data 7": {
        "Cell Voltage 25":[],	
        "Cell Voltage 26":[],
        "Cell Voltage 27":[],
        "Cell Voltage 28":[]
    },
    
    "MMU Cell Voltage Data 8": {
        "Cell Voltage 29":[],	
        "Cell Voltage 30":[],
        "Cell Voltage 31":[],
        "Cell Voltage 32":[]
    },
    
    "MMU Cell Voltage Data 9": {
        "Cell Voltage 33":[],	
        "Cell Voltage 34":[],
        "Cell Voltage 35":[],
        "Cell Voltage 36":[]
    },
    
    "MMU Cell Voltage Data 10": {
        "Cell Voltage 37":[],	
        "Cell Voltage 38":[],
        "Cell Voltage 39":[],
        "Cell Voltage 40":[]
    },
    
    
    "MMU Cell Voltage Data 11": {
        "Cell Voltage 41":[],	
        "Cell Voltage 42":[],
        "Cell Voltage 43":[],
        "Cell Voltage 44":[]
    },
    
    "MMU Cell Voltage Data 12": {
        "Cell Voltage 45":[],	
        "Cell Voltage 46":[],
        "Cell Voltage 47":[],
        "Cell Voltage 48":[]
    }, 
    
    "MMU Cell Temperature Data 1": {
        "Monomer Temperature 1":[],	
        "Monomer Temperature 2":[],
        "Monomer Temperature 3":[],
        "Monomer Temperature 4":[]
    },
    
    "MMU Cell Temperature Data 2": {
        "Monomer Temperature 5":[],	
        "Monomer Temperature 6":[],
        "Monomer Temperature 7":[],
        "Monomer Temperature 8":[]
    },
        
    "MMU Cell Temperature Data 3": {
        "Monomer Temperature 9":[],	
        "Monomer Temperature 10":[],
        "Monomer Temperature 11":[],
        "Monomer Temperature 12":[]
    },
    
    "MMU Cell Temperature Data 4": {
        "Monomer Temperature 13":[],	
        "Monomer Temperature 14":[],
        "Monomer Temperature 15":[],
        "Monomer Temperature 16":[]
    }
}

# check and initaite template
def init():
    for i,v in bmu_template.items():
        for j,jv in v.items():
            if type(jv) is list:
                if len(jv)>0:
                    jv = []
            else:
                for k, kv in jv.items():
                    if len(kv):
                        kv = []

    for i,v in mmu_template.items():
        for j, jv in v.items():
            if len(jv)>0:
                jv = []

def get_bmukeys():
    bmu_keys = []
    for k, v in bmu_template.items():
        for k1, v1 in v.items():
            if type(v1) is dict:
                for k2, v2 in v1.items():
                    bmu_keys.append(k2)
                    # print(k2) 
            else:
                bmu_keys.append(k1)
                # print(k1)
    return bmu_keys


def get_mmukeys():
    mmu_keys = []
    for k, v in mmu_template.items():
        for k1, v1 in v.items():
            if type(v1) is dict:
                for k2, v2 in v1.items():
                    mmu_keys.append(k2)
                    # print(k2) 
            else:
                mmu_keys.append(k1)
                # print(k1)
    return mmu_keys

def get_vsbmskeys():
    ret = []
    for k, v in ext_template.items():
        for k1, v1 in v.items():
            if type(v1) is dict:
                for k2, v2 in v1.items():
                    ret.append(k2)
                    # print(k2) 
            else:
                ret.append(k1)
                # print(k1)
    return ret