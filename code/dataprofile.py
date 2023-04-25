''' 
data profiles

'''

channel_types = (
  "CANBUS-EXT-MBMU",
  "CANBUS-MBMU-SBMU",
  "CANBUS-SBMU-MMU"
)

comm_protocols = (
  "PSA-EXT-CAN-PROTO", 
  "JKE-INT-CAN-PROTO"
)


data_profile_0 = {
  "name": "data-profile-0",
  "desp": "external canbus; internal canbus data between mbmu and sbmus", 
  "nch" : 2,    # number of channels 
  "chn-desp" : [

    # channel 0 
    { 
      "name": "chn-0",
      "chnt": "CANBUS-EXT-MBMU",
      "proto": "PSA-EXT-CAN-PROTO",
      "mbmu-sn": 1000098715,
    },  

    # channel 1 
    { 
      "name": "chn-1",
      "chnt": "CANBUS-MBMU-SBMU",
      "proto": "JKE-INT-CAN-PROTO",
      "nsbmu": 4,
      "mbmu-sn": 1000098715,
      "sbmu-sn": [ 1000098926, 1000098778, 1000098644, 1000099072 ], 
    },
  ]
}

data_profile_1 = {
  "name": "data-profile-1",  
  "desp": "internal canbus data between sbmu and mmus",
  "nch" : 2,  # number of channels 
  "chn-desp" : [

    # channel 0
    { "name": "chn-0",
      "chnt": "CANBUS-SBMU-MMU",
      "proto": "JKE-INT-CAN-PROTO",
      "nmmu": 6,
      "sbmu-sn": 1000098926,
      "mmu-sn": [ 1000106516, 1000106491, 1000106566, 1000106561, 1000099785, 1000099827 ], 
    },

    # channel 1 
    { "name": "chn-1",
      "chnt": "CANBUS-SBMU-MMU",
      "proto": "JKE-INT-CAN-PROTO",
      "nmmu": 6,
      "sbmu-sn": 1000098778,
      "mmu-sn": [1000106590, 1000106580, 1000099638, 1000106546, 1000099170, 1000100050 ], 
    },  
  ]
} 




class DataProfile():
    def __init__(self, dataprofile=None):
        if dataprofile:
            self.name = dataprofile['name']
            self.nch = dataprofile['nch']
            self.chns = []
            for c in dataprofile['chn-desp']:
                self.chns.append(c)
                
    def getNrOfChannel(self):
        return self.nch
    
    def getChannelType(self, chn=None):
        if chn is not None:
            if chn < self.nch:
                return self.chns[chn]['chnt']
            else:
                return None
        else:
            ret = []
            for c in self.chns:
                ret.append(c['chnt']) 
            return ret

    def getChannelName(self, chn=None):
        if chn is not None:
            if chn < self.nch:
                return self.chns[chn]['name']
            else:
                return None 
        else:    
            ret = []
            for c in self.chns:
                ret.append(c['name']) 
            return ret

    def getChannelProto(self, chn=None):
        if chn is not None:
            if chn < self.nch:
                return self.chns[chn]['proto']
            else:
                return None 
        else:    
            ret = []
            for c in self.chns:
                ret.append(c['proto']) 
            return ret
    
    def getChannelInfo(self, chn=None):
        if chn is not None:
            if chn < self.nch:
                return self.chns[chn]
            else:
                return None 
        else:    
            ret = []
            for c in self.chns:
                ret.append(c) 
            return ret
    