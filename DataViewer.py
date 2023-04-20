#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#import sys
#sys.path.insert(0,'./code')
from dataprofile import *
from dataparser import *
from bmsdataset import * 
from bmssession import *
from xlsxdumper import *
from util import *
from templates import *

from tableviewer import * 
from plot import *

import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure 
       
class DataViewLayout():
    
    def __init__(self, root_W=1200, root_H=600):
        
        self.root_W = 1200
        self.root_H = 600 
        self.statusframe_H = 30
        self.controlframe_W = 240 
        self.padx = 5
        self.pady = 5
        
        self.recalc()
        
    def recalc(self, root_W=None, root_H=None): 
        
        if root_W:
            self.root_W = root_W
            
        if root_H:
            self.root_H = root_H
        
        self.dataframe_W = self.root_W - self.controlframe_W
        self.dataframe_H = self.root_H - self.statusframe_H 
        self.controlframe_H = self.root_H - self.statusframe_H 
         
class DataViewer():
    def __init__(self, root=tk.Tk(), title="Data Viewer"):
          
        ## initialize root/main frame  
        self.layout = DataViewLayout()
        self.root = root
        self.root.geometry(f"{self.layout.root_W}x{self.layout.root_H}") # set the root dimensions
        self.root.title(title)
        self.root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.
        #root.resizable(0, 0) # makes the root window fixed in size.
        
        ## data profile
        self.dataprofile_setting = 1  # data profile { 0 | 1 } 
        
        ## bms dataset 
        self.bms_ds = None 
        
        ## session
        self.session = None

        ## initialize menu
        m = tk.Menu(self.root)
        self.root.config(menu=m)
        self.file_menu = tk.Menu(m, tearoff=False) # Add Menu Dropdown
        m.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open raw data file", command=lambda: self.__loaddata())
        self.file_menu.add_command(label="Export as excel", command=lambda: self.__savedata(filetype='xlsx')) 
        self.file_menu.add_command(label="Export as json", command=lambda: self.__savedata())  
        self.file_menu.add_separator()
        self.file_menu.add_command(label="New session", command=lambda: self.__newsession())
        self.file_menu.add_command(label="Open session", command=lambda: self.__opensession()) 
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save session", command=lambda: self.__savesession()) 
        self.file_menu.add_command(label="Save session as") #, command=lambda: self.__saveassession)  
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close session") #, command=lambda: self.__closesession) 
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.destroy)
    
        self.setting_menu = tk.Menu(m, tearoff=False) # Add Menu Dropdown
        m.add_cascade(label="Setting", menu=self.setting_menu)
        self.setting_menu.add_command(label="Select Data Profile", command=lambda: self.__sel_dataprofile())
         
        
        # Data Frame for TreeView
        self.dataframe = tk.LabelFrame(root, text="Battery Data", name="dataframe")  # frame1
        self.dataframe.place(width=self.layout.dataframe_W, height=self.layout.dataframe_H)  # height=600, width=1010

        # Control Frame for control board
        self.controlframe = tk.LabelFrame(root, text="Control Board", name="controlframe")  # file_frame
        self.controlframe.place(width=self.layout.controlframe_W, height=self.layout.controlframe_H, 
                                x= self.layout.root_W-self.layout.controlframe_W) #,  relx=0.8) # rely=0, # height=600, width=240, relx=0.8 
         
        # Radio widgets, channels, 
        self.chn=tk.IntVar()
        self.chn.set(0)
        self.chn_frame = tk.LabelFrame(self.controlframe, text="Channels")
        self.chn_frame.place(height=60, width=220, relx=0.04, y = 10) # rely=0.02
        self.R0 = tk.Radiobutton(self.chn_frame, text="Channel 0", variable=self.chn, value=0, padx=5, command=self.chn_sel)
        self.R0.pack(side=tk.LEFT)
        self.R1 = tk.Radiobutton(self.chn_frame, text="Channel 1", variable=self.chn, value=1, padx=5, command=self.chn_sel)
        self.R1.pack(side=tk.LEFT)
        
        # Radio widgets, data tables, internal CANBus
        self.tbi=tk.IntVar() 
        # self.tbi.set(0)
        self.table_frame = tk.LabelFrame(self.controlframe, text="Tables- Internal Bus")
        self.table_frame.place(height=260, width=220, relx=0.04, y = 80 ) #rely=0.15) # rely=0, 

        self.VSBMU_R = tk.Radiobutton(self.table_frame, text="VS-BMS (E-CANBus)", variable=self.tbi, value=7, padx=5, command=self.table_sel) #, ommand=sel)
        # self.VSBMU_R.grid(row=1, column=0, columnspan =2, sticky=tk.W, ipady=5, pady=5 )  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)
         
        self.BMU_R = tk.Radiobutton(self.table_frame, text="BMU", variable=self.tbi, value=0, padx=5, command=self.table_sel) #, ommand=sel)
        # self.BMU_R.grid(row=2, column=0, columnspan =2, sticky=tk.W) #, ipady=5, pady=5 )  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

        self.MMU0_R = tk.Radiobutton(self.table_frame, text="MMU 1", variable=self.tbi, value=1, padx=5, command=self.table_sel) #, ommand=sel)
        # self.MMU0_R.grid(row=3, column=0)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

        self.MMU1_R = tk.Radiobutton(self.table_frame, text="MMU 2", variable=self.tbi, value=2, padx=5, command=self.table_sel) #, ommand=sel)
        # self.MMU1_R.grid(row=3, column=1)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

        self.MMU2_R = tk.Radiobutton(self.table_frame, text="MMU 3", variable=self.tbi, value=3, padx=5, command=self.table_sel) #, ommand=sel)
        # self.MMU2_R.grid(row=4, column=0)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

        self.MMU3_R = tk.Radiobutton(self.table_frame, text="MMU 4", variable=self.tbi, value=4, padx=5, command=self.table_sel) #, ommand=sel)
        # self.MMU3_R.grid(row=4, column=1)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

        self.MMU4_R = tk.Radiobutton(self.table_frame, text="MMU 5", variable=self.tbi, value=5, padx=5, command=self.table_sel) #, ommand=sel)
        # self.MMU4_R.grid(row=5, column=0)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

        self.MMU5_R = tk.Radiobutton(self.table_frame, text="MMU 6", variable=self.tbi, value=6, padx=5, command=self.table_sel) #, ommand=sel)
        # self.MMU5_R.grid(row=5, column=1)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)
        
        
        self.redraw_tableframe()
        
        # data tables - external CANBus
        #self.e_table_frame = tk.LabelFrame(self.controlframe, text="Tables- External Bus")
        #self.e_table_frame.place(height=60, width=220, relx=0.04, y = 80+195+10 ) #rely=0.15) # rely=0, 
          
        #self.BMU_R = tk.Radiobutton(self.e_table_frame, text="VS-BMU", variable=self.tbi, value=0, padx=5, command=self.table_sel) #, ommand=sel)
        #self.BMU_R.grid(row=1, column=0, columnspan =2, sticky=tk.W, ipady=5, pady=5 )  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)
         
        # toolkit frame
        self.toolkit_frame = tk.LabelFrame(self.controlframe, text="Toolkit")
        self.toolkit_frame.place(height=200, width=220, relx=0.04, y=350) # rely=0,  
        self.plot_btn = tk.Button(self.toolkit_frame, text="Plot", padx=10, command=lambda: self.draw_plot(df=self.bms_ds))
        self.plot_btn.place(x=10,y=15)
        
        # session frame
        self.session_frame = tk.LabelFrame(self.controlframe, text="Session")
        self.session_frame.place(height=370, width=220, relx=0.04, y=560) # rely=0,  
        self.label_session = ttk.Label(self.session_frame, text="No data")
        self.label_session.place(rely=0.02, relx=0)
      
        # status frame
        self.statusframe = tk.LabelFrame(self.root, name="statusframe")
        self.statusframe.place(height=self.layout.statusframe_H, relwidth = 1, y=self.layout.root_H-self.layout.statusframe_H )
        # rely=0.96) # rely=0, , anchor="sw",  width=1270,  , 

        # The file/file path text
        self.label_file = ttk.Label(self.statusframe, text="No File Selected")
        self.label_file.place(rely=0, relx=0)
     
        # Treeview Widget
        self.tv = ttk.Treeview(self.dataframe)
        self.tv.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

        self.treescrolly = tk.Scrollbar(self.dataframe, orient="vertical", command=self.tv.yview) # command means update the yaxis view of the widget
        self.treescrollx = tk.Scrollbar(self.dataframe, orient="horizontal", command=self.tv.xview) # command means update the xaxis view of the widget
        self.tv.configure(xscrollcommand=self.treescrollx.set, yscrollcommand=self.treescrolly.set) # assign the scrollbars to the Treeview Widget
        self.treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        self.treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
     
        # instantiate table viewer with Tree View 
        self.tblv = tableviewer(tv=self.tv) 
    
        self.root.bind("<Configure>", self.resize)
     
    ## redraw control frame with data profile setting
    def redraw_tableframe(self):
        
        print("profile {}".format(self.dataprofile_setting))
        print("chn {}".format(self.chn.get()))
        
        if self.dataprofile_setting == 0:   
            if self.chn.get() == 0: 
                self.table_frame.configure(text="Tables- Ext2MBMU")
                self.BMU_R.grid_forget() # (row=2, column=0, columnspan =2, sticky=tk.W)  
                self.MMU0_R.grid_forget() # (row=3, column=0)   
                self.MMU1_R.grid_forget() # (row=3, column=1)   
                self.MMU2_R.grid_forget() # (row=4, column=0)   
                self.MMU3_R.grid_forget() # (row=4, column=1)   
                self.MMU4_R.grid_forget() # (row=5, column=0)   
                self.MMU5_R.grid_forget() # (row=5, column=1) 
                self.tbi.set(7)
                self.VSBMU_R.grid(row=1, column=0, columnspan =2, sticky=tk.W, ipady=5, pady=5 )   
            else: 
                self.table_frame.configure(text="Tables- MBMU2SBMU")
                self.VSBMU_R.grid_forget() 
                self.MMU4_R.grid_forget() # (row=5, column=0)   
                self.MMU5_R.grid_forget() # (row=5, column=1) 
                self.tbi.set(0)
                self.BMU_R.grid(row=2, column=0, columnspan =2, sticky=tk.W)  
                self.MMU0_R.grid(row=3, column=0)   
                self.MMU1_R.grid(row=3, column=1)   
                self.MMU2_R.grid(row=4, column=0)   
                self.MMU3_R.grid(row=4, column=1) 
        else: 
            self.table_frame.configure(text="Tables- Internal Bus") 
            self.VSBMU_R.grid_forget()
            self.tbi.set(0)
            self.BMU_R.grid(row=2, column=0, columnspan =2, sticky=tk.W)  
            self.MMU0_R.grid(row=3, column=0)   
            self.MMU1_R.grid(row=3, column=1)   
            self.MMU2_R.grid(row=4, column=0)   
            self.MMU3_R.grid(row=4, column=1)   
            self.MMU4_R.grid(row=5, column=0)   
            self.MMU5_R.grid(row=5, column=1)   

     
    def resize(self, event): 
        # print("widget {}, width {}, height {}".format(event.widget.winfo_name() ,  event.width, event.height))
        if event.widget.winfo_name() == "tk" :  # is root            
            if self.layout.root_W != event.width or self.layout.root_H != event.height : 
                # print("widget {} resized to, width {}, height {}".format(event.widget.winfo_name(), event.width, event.height))
                self.layout.root_W = event.width 
                self.layout.root_H = event.height
                self.layout.recalc()
                # update all widgets 
                self.update_widgetsize()
        
    def update_widgetsize(self): 
        self.dataframe.place(width=self.layout.dataframe_W, height=self.layout.dataframe_H) 
        self.controlframe.place(width=self.layout.controlframe_W, height=self.layout.controlframe_H, 
                                x= self.layout.root_W-self.layout.controlframe_W) #,  relx=0.8) # rely=0, # height=600, width=240, relx=0.8  
        self.statusframe.place(height=self.layout.statusframe_H, relwidth = 1, y=self.layout.root_H-self.layout.statusframe_H )# r
         
    def chn_sel(self):
        self.redraw_tableframe()
        self.__update_to_tableviewer()
          
    def table_sel(self):
        self.__update_to_tableviewer() 
           
    def run(self):
        self.root.mainloop()
      
    def __newsession(self):
        
        # popup box for input session name
        session_name = simpledialog.askstring("New Session", "Please give a session name:", parent=self.root)
             
        if session_name is None:
            return
          
        if self.session:
            self.session = None
        
        # create new session
        self.session = BMS_Session(name=session_name)
        
        # put current data in dataframe in the session 
        if self.bms_ds:
            fname = self.label_file['text']
            self.session.insert(record={'filename':fname, 'frames':self.bms_ds.frames, 'rtime':self.bms_ds.rtime})
            records = self.session.get_records()
            label_text = ""
            for r in records:
                fn = r['filename']
                label_text +=f"{fn}\n" 
            self.label_session['text'] = label_text 
         
        # update the status label 
        self.label_file['text'] = f"{self.session.name}" 
        
        # update the session frame 
        self.session_frame['text']= f"Session: {self.session.name}"
    
    
    def __sel_dataprofile(self):
        rb = tk.Toplevel(self.root)
        rb.wm_title("Select Data Profile")
        rb.geometry("350x200")
        
        radio = tk.IntVar()
        radio.set(self.dataprofile_setting)
        
        rb_label = ttk.Label(rb, text="Select correct data profile before loading raw data")
        rb_label.grid(row=0, column=0, sticky = tk.W, padx = 5, pady = 2)
        
        R1 = tk.Radiobutton(rb, text="profile 0 - externl CAN bus", variable=radio, value=0) #, command=selection)  
        R1.grid(row=1, column=0, sticky = tk.W, padx = 5, pady = 2 ) 
  
        R2 = tk.Radiobutton(rb, text="profile 1 - internal CAN bus", variable=radio, value=1) # ,  command=selection)  
        R2.grid(row=2, column=0, sticky = tk.W, padx = 5, pady = 2 ) 
  
        def _rb_quit():
            self.dataprofile_setting = radio.get() 
            self.redraw_tableframe() 
            rb.quit()     # stops mainloop
            rb.destroy()  # this is necessary on Windows to prevent
  
        rb_btn = tk.Button(rb, text="Select", padx=10, command=lambda: _rb_quit())
        rb_btn.grid(row=3, column=0, sticky = tk.W, padx = 5, pady = 12 ) 
         
        self.root.mainloop() 
          
    
    def __savesession(self):
         self.session.save()
  
    def __opensession(self):
        filename = filedialog.askopenfilename( # initialdir="/",
                                      title="Select A File",
                                      filetype=(("Session (.json) files", "*.json") ,("All Files", "*.*")))
        if filename is None:
            return 
        
        with open(filename, 'r') as f:
            data = json.load(f)
            
        if self.session:
            self.session = None
         
        self.session = BMS_Session(name=data['name']) 
        records = data['records']
            
        if self.bms_ds:
            self.bms_ds = None
        
        # re-generate session
        label_text = ""
            
        self.bms_ds = BMS_Dataset(name="bms-dataset")
        for r in records:
            data_filename = r['filepath']
            with open(data_filename, 'r') as f:
                lines = f.readlines()   # lines
                    
            for line in lines:    
                if not line:
                    break

                try:    
                    self.bms_ds.insert(ojson=BMS_frame(line=line).dump_to_json())
                except Exception as e:
                    print(e)
                    continue
            
            self.session.insert(record={'filename':data_filename, 'frames':len(lines), 'rtime':self.bms_ds.rtime})  
            records = self.session.get_records()
             
            fn = r['filename']
            label_text +=f"{fn}\n" 
            self.label_session['text'] = label_text 

        self.__update_to_tableviewer()
        self.label_file['text'] = self.session.name
         
        
    def __loaddata(self):
        fp = FileProcessor()
        rdh = RawDataHolder(filename=fp.filename, data=fp.df)
         
        ## disable profile setting 
        self.setting_menu.entryconfig("Select Data Profile", state="disabled")
    
        if self.bms_ds is None:
            self.bms_ds = BMS_Dataset(name="bms-dataset", dataprofile=DataProfile(dataprofile=data_profile_0)) 
            # print(self.bms_ds.ds[0]['bmu'])
     
        if rdh.isRawData == True:
            lines = rdh.rawdata 
            # print("__loaddata: lines = {}".format(len(lines)))

            for line in lines:    
                if not line:
                    break

                try:    
                    self.bms_ds.insert(ojson=BMS_frame(line=line).dump_to_json())
                except Exception as e:
                    print(e)
                    continue
                      
            if self.session:
                self.session.insert(record={'filename':fp.filename, 'frames':len(lines), 'rtime':self.bms_ds.rtime})  
                records = self.session.get_records()
                label_text = ""
                for r in records:
                    fn = r['filename']
                    label_text +=f"{fn}\n"
                
                self.label_session['text'] = label_text 
                #left = tk.Label(self.session_frame, text=label_text)
                #left.pack(side = tk.LEFT)
                #print(records)
                
        self.__update_to_tableviewer()
        
        if self.session is None:
            self.label_file['text'] = fp.filename
        
    def __update_to_tableviewer(self):    
        
        tbs = ["BMU", "MMU 1", "MMU 2", "MMU 3", "MMU 4", "MMU 5", "MMU 6", "VS-BMS (E-CANBus)"] 
        
        print("Channel {}".format(self.chn.get()))
        print("Table {}".format(tbs[self.tbi.get()]))
        
        _channel = self.chn.get()
        _tableidx = self.tbi.get()
        if _tableidx ==0: # bmu
            _tablename = list(self.bms_ds.ds[_channel].keys())[_tableidx]
            df = self.bms_ds.ds[_channel][_tablename] 
            titles = self.bms_ds.get_title(ds=df, keys=get_bmukeys()) # get_bmukeys()
        elif _tableidx == 7: # VS-BMS
            _tablename = 'ext'
            print(self.bms_ds.ds[_channel].keys())
            df = self.bms_ds.ds[_channel][_tablename] 
            titles = self.bms_ds.get_title(ds=df, keys=get_vsbmskeys()) # get_bmukeys() 
        else:  # mmu
            df = self.bms_ds.ds[_channel]["mmus"][_tableidx-1]
            titles = self.bms_ds.get_title(ds=df, keys=get_mmukeys())
            
        self.tblv.update(df=df, titles=titles) 
        self.dataframe.configure(text="Cahnnel {}, {}".format(_channel, tbs[_tableidx]))
   
    def __savedata(self, filetype='json'):
        fp = FileProcessor(disable_load=True)
        fp.savefile(data=self.bms_ds, filetype=filetype)
        
    
    # df is objectof BMS_Dataset  
    def draw_plot(self, df=None):
     
        _channel = self.chn.get()
        _table_idx = self.tbi.get()

        if _table_idx == 0:
            elements = [ 
                    ("Average Cell Voltage", "0.001V", "100ms"), 
                    ("Average Monomer Temperature", "0.1C", "100ms"), 
                    ("Total Battery Voltage", "0.05V", "100ms"),
                    ("Total Battery Current", "0.05A", "100ms")]
            plot = Plot(elements=elements) 
        elif  _table_idx == 7:
            elements = [ 
                    ("BMS Mode Request", "", "200ms"), 
                    ("BMS IMD Disabled", "", "200ms"), 
                    ("BMS Mode", "", "500ms"),
                    ("Number of Strings Connected", "", "500ms"),
                    ("Battery System Voltage", "0.1V", "500ms"),
                    ("Battery System Current", "0.1A", "500ms")]
            plot = Plot(elements=elements)
        else:
            elements = [
                    ("Average Cell Voltage", "0.001V", "100ms"), 
                    ("Average Monomer Temperature", "0.1C", "100ms"), 
                    ("Total Battery voltage (Single Cumulative Sum)", "0.05V", "100ms"),
                    ("Total Battery Current", "0.05A", "100ms"),]  
                    #("Cell Voltage 1", "0.001V", "100ms")
            plot = Plot(elements=elements)
            plot.set_mmu_cell_voltemp()
        
        plot.draw(df=df, channel=_channel, table_idx=_table_idx)


# In[ ]:


if __name__ == "__main__":
    
    app = DataViewer()
    
    app.run()

