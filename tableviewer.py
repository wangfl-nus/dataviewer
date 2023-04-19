import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd
import numpy as np

class tableviewer:
    def __init__(self, tv=None):
        self.tv = tv
        
    def update(self, clear=True, df=None, titles=None):
             
        if clear == True:
            self.clear()
         
        # update data to the table viewer
        if df:
            # print(type(df))
            if type(df) is dict: 
                self.__handle_ds(df, titles)  # bms dataset
            else:
                self.__handle_df(df)  # pands dataframe
      
    def clear(self):
        self.tv.delete(*self.tv.get_children())
        return None
     
    # handle bms dataset 
    def __handle_ds(self, df=None, titles=None):
        
        # dataset: channel, bmu or mmu 
        # update_to_tkviewer(df=dumper)
         
        def __get_titles(ds):
            ret = []
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
        
        def __ds_tolist(ds, titles):
            ret = [] # rows

            _coln = len(titles)
            # _l = list(ds.keys())[0]
            # _t = list(ds.keys())[0]  # _l  
            _d = ds[list(ds.keys())[0]]  # _t
            # __l = list(ds[list(ds.keys())[0]].keys())  # _d
            __t = list(_d.keys())[0]  # __l
            # print(_d[__t]) 
            _rown = len(_d[__t]) # number of rows 
            #print("title: {}, rows: {}".format(__t, _rown))
            #print(list(ds.keys()))

            for r in range(_rown):
                count = 0
                row = []
                for col in range(_coln):
                    for k, v in ds.items(): 
                        if k == "Invalid Frame ID": 
                            continue 
                        if type(v) is dict:
                            for k1, v1 in v.items():
                                if type(v1) is dict:
                                    for k2,v2 in v1.items():  
                                        if k2 == titles[col]: # print(k2)
                                            try:
                                                row.append(v2[r])
                                            except: 
                                                row.append('')
                                            count += 1
                                else:
                                    if k1 == 'rtime': 
                                        continue
                                    # print(k1)
                                    if k1 == titles[col]:
                                        try:
                                            row.append(v1[r])
                                        except:
                                            row.append('')
                                        count += 1
                        else:
                            print("error")
                            break

                ret.append(row) 
                
            return ret
        
        # handle titles 
        if titles:
            tl = titles
        else:
            tl = __get_titles(ds=df)
             
        self.tv["column"] = tl  # heading 
        self.tv["show"] = "headings"
        for column in self.tv["columns"]:
            self.tv.heading(column, text=column) # let the column heading = column name
            self.tv.column(column, stretch=False)

        df_rows = __ds_tolist(ds=df, titles=tl) # convert to list of raws
          
        for row in df_rows:
            self.tv.insert("", "end", values=row) # inserts each list into the treeview. For parameters 
                                              # see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
  
        return None

    ## hande df(excel) datefrome
    def __handle_df(self, df=None):
        # handle heading, merge rows 0~3 values   
        num_of_col = len(df.values[0])
        for i in range(num_of_col):
            if df.values[2][i] is np.nan:
                df.values[2][i] = df.values[3][i] 

        self.tv["column"] = list(df.values[2])  # list(df.columns)
        self.tv["show"] = "headings"
        for column in self.tv["columns"]:
            self.tv.heading(column, text=column) # let the column heading = column name
            self.tv.column(column, stretch=False)

        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        for row in df_rows[4:]:
            self.tv.insert("", "end", values=row) # inserts each list into the treeview. For parameters 
                                             # see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        return None

    