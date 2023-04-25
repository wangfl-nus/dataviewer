''' Raw data holder

raw data from .txt file or xlsx, cscv files

Return: a list of lines in raw data file
        or pandas df format from xlsx or csv  
'''
from bmsdataset import * 
from xlsxdumper import *
 
from tkinter import filedialog, messagebox

import pandas as pd
import numpy as np
 
class RawDataHolder:
    def __init__(self, filename='', data=None):
        if data:
            self.filename = filename
            self.rawdata  = data  
            self.isRawData = False
            if type(data) is list:
                self.isRawData = True

''' File Processor

Open or Save data file 

'''    
class FileProcessor:
    def __init__(self, disable_load=False):
        self.filename = None
        self.isTxt = False
        self.df = None 
        if disable_load == False:
            self.loaddata()
     
    def loaddata(self):
        
        """This Function will open the file explorer and assign the chosen file path to label_file"""
    
        filename = filedialog.askopenfilename( # initialdir="/",
                                              title="Select A File",
                                              filetype=(("raw (.txt) data files", "*.txt"), ("xlsx files", "*.xlsx"),("All Files", "*.*")))
        # update status bar
        # label_file["text"] = filename
        self.filename = filename

        """If the file selected is valid this will load the file into the Treeview"""

        file_path = self.filename # label_file["text"]
        self.isTxt = False

        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".txt":
                self.isTxt = True 
                with open(excel_filename, 'r') as f:
                    self.df = f.readlines()   # lines 
            elif excel_filename[-4:] == ".csv":
                self.df = pd.read_csv(excel_filename)
            else:
                self.df = pd.read_excel(excel_filename)

        except ValueError:
            messagebox.showerror("Information", "The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            messagebox.showerror("Information", f"No such file as {file_path}")
            return None
 
        '''
        if self.isTxt:
             handle_lines(lines=lines) 
        else:
            clear_data() 
            handle_df(df=df)
        '''
        return None
 
    def savefile(self, data=None, filetype='json'):
        
        if filetype=='json':
            de=".json"
            ft=(("json files", "*.json"), ("All files", "*.*"),)
        elif filetype=='xlsx':
            de=".xlsx"
            ft=(("xlsx files", "*.xlsx"), ("All files", "*.*"),)
  
        file_path = filedialog.asksaveasfilename(
                    defaultextension=de,   # ".json" 
                    filetypes=ft)
        
        print("Save file to "+file_path)
        
        if filetype=='json':
            if data:
                data.save(fpath=file_path)

        elif filetype=='xlsx':
            # generate dumper 
            print("create xlsx dumper")
            d2x = BMS_ds2xlsx(src=data, fpath=file_path)
            d2x.get_xlsxDataFrame().save()
             
# dump data from bms_ds to xlsx 
class BMS_ds2xlsx():
    def __init__(self, src=None, fpath="temp.xlsx"):
        self.xlsx_df = xlsx_dumper(view="new", fname=fpath) 
        
        def _toxlsx(src=src): 
            # src = bms_ds
            # des = self.xlsx_df
            wb=self.xlsx_df.wb
            xdf=self.xlsx_df.params
            ds=src.ds
             
            # handle bmu data
            def handle_bmu(des, src):
                # print("des structure:") 
                ws=des['ws']
                num_of_col = ws.max_column
                cells = ws.cell 
                for i in range(1,num_of_col): 
                    if cells(row=5, column=i).value is None: 
                        # ret.append(cells(row=4, column=i).value)
                        key = cells(row=4, column=i).value
                    else:
                        # ret.append(cells(row=5, column=i).value)    
                        key = cells(row=5, column=i).value

                    for k,v in src.items():
                        # print(k)
                        if type(v) is dict:
                            for k1, v1 in v.items():
                                #print("... "+k1)
                                if type(v1) is dict:
                                    for k2, v2 in v1.items():
                                        if k2==key:
                                            #print("... "+k2)
                                            # copy_col(cells, i, v2)
                                            for r in range(len(v2)):
                                                cells(row=r+6, column=i).value = v2[r]
                                            break; 
                                else:
                                    if k1==key:
                                        #print("... "+k1)
                                        # copy_col(cells, i, v1)
                                        for r in range(len(v1)):
                                            cells(row=r+6, column=i).value = v1[r]
                                        break
            # handle mmu data              
            def handle_mmu(des, src):
                ws=des['ws']
                num_of_col = ws.max_column
                cells = ws.cell 
                for i in range(1,num_of_col): 
                    key = cells(row=4, column=i).value 
                    for k,v in src.items():
                        # print(k)
                        if type(v) is dict:
                            for k1, v1 in v.items():
                                # print("... "+k1) 
                                if k1==key:
                                    # print("... "+k1)
                                    # copy_col(cells, i, v1)
                                    for r in range(len(v1)):
                                        cells(row=r+5, column=i).value = v1[r]
                                    break
             
            # handle channels 
            for c in range(2):
                s = ds[c]  
                d = xdf[c]

                handle_bmu(des=d['bmu'], src=s['bmu'])

                # generate mmu sheet
                sl = len(s['mmus'])
                dl = len(d['mmus'])

                ws = d['mmus'][-1]['ws'] # the last mmu 
                title = ws.title[:8] 

                while(dl<sl):
                    # print(ws.title)
                    newws = wb.copy_worksheet(ws) # self.wb[ws]
                    newws.title=title+str(dl)
                    d['mmus'].append({"ws":newws, "rows":{}})
                    ws = newws
                    dl += 1

                for m in range(len(s['mmus'])):
                    handle_mmu(des=d['mmus'][m], src=s['mmus'][m])
             
            return  
         
          
        _toxlsx(src=src)
      
     
    def get_xlsxDataFrame(self):
        return self.xlsx_df
   
        

if __name__ == "__main__":
    from dataparser import *
    from bmsdataset import * 
     
    fp = FileProcessor()
    rdh = RawDataHolder(filename=fp.filename, data=fp.df)
    
    bms_ds = BMS_Dataset(name="bms-dataset")
    
    if rdh.isRawData == True:
        lines = rdh.rawdata
    
        for line in lines:    
            if not line:
                break

            try:    
                bms_ds.insert(ojson=BMS_frame(line=line).dump_to_json())
            except Exception as e:
                print(e)
                continue

    bms_ds.info()
    
    