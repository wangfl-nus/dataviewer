import os
import json

class BMS_Session:
    def __init__(self, name="default seesion", records=None):
        self.name = name
        if records:
            self.records=records
        else:    
            self.records=[]
            
    # insert a dataset (data file)
    def insert(self, record=None):
        if record:
            d = {}
            if 'filename' in record.keys():
                d['filepath'] = record['filename'] 
                d['filename'] = os.path.basename(record['filename']) 
            if 'frames' in record.keys():  # numver of lines 
                d['frames'] = record['frames']
            if 'rtime' in record.keys(): # duration in 0.1ms, e.g 600000    
                d['rtime'] = record['rtime']
                
            self.records.append(d)    
    
    def get_records(self):
        return self.records
    
    def save(self, filepath=None):
        if filepath:
            fp =  filepath
        else:
            fp = self.name+".json"
        with open(fp, 'w') as f:
            data = {"name":self.name, "records":self.records}
            json.dump(data, f)
            