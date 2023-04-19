import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure 
       
'''
elements

[
 (<column name>, <unit>, <interval>), 

 ("Average Cell Voltage", "0.001V", "100ms"),
 ("Average Monomer Temperature", "0.1C", "100ms"),
  
 ...
]
  
'''
class Plot:
    def __init__(self, elements=[]):
        self.set_elements(elements=elements)  
         
    def set_elements(self, elements=[]):
        self.elements = elements
        self.current = 0
        self.df = None
        self.channel = 0
        self.table_idx = 0
        self.mmu_cell_voltemp = False

    def set_mmu_cell_voltemp(self, value=True):
        self.mmu_cell_voltemp = value
        
    def draw(self, root=None, df=None, channel=0, table_idx=0):
        self.df = df
        self.channel = channel
        self.table_idx = table_idx
         
        col_names = []
        units = []
        intvals = []
        for i in self.elements:
            col_names.append(i[0]) 
            units.append(i[1])
            intvals.append(i[2])
        
        _channel = self.channel
        _table_idx = self.table_idx

         # get values of one column 
        cl = self.df.getValueByColumn(chn=_channel, sheetNo=_table_idx, colname=col_names[0]) # "Average Cell Voltage")
        
        # title 
        _chnT = "Channel 0" if _channel == 0 else "Channel 1"
        if _table_idx == 0:
            _sheetT = "BMU" 
        elif _table_idx == 7:
            _sheetT = "VS-BMS (E-CANBus)"
        else:
            _sheetT = f"MMU {_table_idx}" 

        top1 = tk.Toplevel(root)  
        top1.wm_title(f"Plot - {col_names[0]}, {_chnT}, {_sheetT}")  

        fig = Figure(figsize=(6, 4), dpi=100)
        graph = fig.add_subplot()
        graph.plot(range(len(cl)), cl)

        canvas = FigureCanvasTkAgg(fig, master=top1)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, top1)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        def on_key_press(event):
            key_press_handler(event, canvas, toolbar)

        canvas.mpl_connect("key_press_event", on_key_press)

        def _quit():
            top1.quit()     # stops mainloop
            top1.destroy()  # this is necessary on Windows to prevent

        # create frame for radios, button arrangement 
        plot_frame = tk.LabelFrame(master=top1, borderwidth = 0, highlightthickness = 0)
        plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)  

        button = tk.Button(master=plot_frame, text="Quit", command=_quit)
        button.pack(side=tk.RIGHT, padx=50)

        acvt=tk.IntVar()

        def figsel():
            vt = acvt.get()
            if vt < len(self.elements): 
                colname = col_names[vt]
                top1.wm_title(f"Plot - {colname}, {_chnT}, {_sheetT}")  
                cl = self.df.getValueByColumn(chn=_channel, sheetNo=_table_idx, colname=colname) 
            else:
                if _table_idx > 0:
                    # handle cell voltemp
                    if vt ==5:
                        selection = comboVol.get()
                        colname = f"Cell Voltage {selection}"
                        #print("MMU Cell Voltage {}".format(selection))
                    elif vt ==6: 
                        selection = comboTemp.get()
                        colname = f"Monomer Temperature {selection}"
                        #print("MMU Cell Temperature {}".format(selection)) 
                    else:
                        return
                    top1.wm_title(f"Plot - {colname}, {_chnT}, {_sheetT}")
                    cl = self.df.getValueByColumn(chn=_channel, sheetNo=_table_idx, colname=colname)
                else:
                    return

            graph.clear()
            graph.plot(range(len(cl)), cl)
            canvas.draw()

        for i in range(len(self.elements)):
            acvr = tk.Radiobutton(master=plot_frame, text=self.elements[i][0], variable=acvt, value=i, padx=5, command=figsel) #, ommand=sel)
            acvr.pack(side=tk.LEFT) # grid(row=2, column=0)  #  pack(anchor=tk.W) # side=tk.LEFT) # anchor = tk.W)

            
        def vol_modified(event):
            acvt.set(5)
            #selection = comboVol.get()
            #print("vol_modified {}".format(selection))
            figsel()
            
        def temp_modified(event):
            acvt.set(6)
            #selection = comboVol.get()
            #print("temp_modified {}".format(selection)) 
            figsel()
                
        # mmu cell vol and temp 
        if _table_idx > 0:
            if self.mmu_cell_voltemp == True:
                acvr = tk.Radiobutton(master=plot_frame, text="Cell Voltage ", variable=acvt, value=5, padx=5, command=figsel) #, ommand=sel)
                acvr.pack(side=tk.LEFT) 
                # combox 
                comboVol = ttk.Combobox(plot_frame, state="readonly", values=list(range(1,31)), width=4)
                comboVol.current(0)
                comboVol.pack(side=tk.LEFT)
                comboVol.bind('<<ComboboxSelected>>', vol_modified)
                acvr = tk.Radiobutton(master=plot_frame, text="Monomer Temperature ", variable=acvt, value=6, padx=5, command=figsel) #, ommand=sel)
                acvr.pack(side=tk.LEFT) 
                comboTemp = ttk.Combobox(plot_frame, state="readonly", values=list(range(1,5)), width=4)
                comboTemp.pack(side=tk.LEFT) 
                comboTemp.bind('<<ComboboxSelected>>', temp_modified)
                comboTemp.current(0)
                 
        tk.mainloop() 
