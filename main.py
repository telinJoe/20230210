# GUI of line graph

import os
import datetime
import csv
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from tkcalendar import Calendar
import pandas as pd

class application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        #GUI
        self.master.title("GUI")
        self.master.resizable(False, False)
        self.master.geometry('1280x680')
        
        #labelFrame of graph
        self.graphLF = tk.LabelFrame(self.master, width=1000, height=600, borderwidth=3, font=('arial',12,'bold'))
        self.graphLF.grid(row=0, column=0, rowspan=2, padx=10, pady=30)
        self.fig = Figure(figsize=(9.7, 5.7), facecolor='lavender')
        self.ax_configure()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graphLF)
        self.canvas.get_tk_widget().place(x=10, y=10)
        
        #labelFrame of configure
        self.configureLF = tk.LabelFrame(self.master, width=250, height=400, borderwidth=3, font=('arial',12,'bold'))
        self.configureLF.grid(row=0, column=1, rowspan=1, padx=10, pady=30, sticky=tk.N)
        self.text_info = ttk.Label(self.configureLF, text='Input folder', font=("arial",12))
        self.text_info.place(y=20)
        self.folder_path = tk.StringVar(value=os.getcwd())
        self.folder_path_entry = ttk.Entry(self.configureLF, textvariable=self.folder_path, width=30, state='disabled')
        self.folder_path_entry.place(y=40)
        self.Browse_button = tk.Button(self.configureLF, text='...', width=2, command=self.chooseFolder)
        self.Browse_button.place(x=218, y=35)
        self.currentDate = tk.StringVar()
        self.currentDateDate_entry = ttk.Entry(self.configureLF, textvariable=self.currentDate, width=10, state='disabled')
        self.currentDateDate_entry.place(x=80, y=82)
        self.lastDay_button = tk.Button(self.configureLF, text='◀', width=2, command=lambda: self.moveDay(-1))
        self.lastDay_button.place(x=50, y=80)
        self.nextDay_button = tk.Button(self.configureLF, text='▶', width=2, command=lambda: self.moveDay(1))
        self.nextDay_button.place(x=160, y=80)
        self.calendar = Calendar(self.configureLF, date_pattern="ymmdd")
        self.calendar.place(x=10,y=120)
        self.calendar_button = tk.Button(self.configureLF, text='choose', width=10, command=lambda: self.showPlot(1))
        self.calendar_button.place(x=30, y=300)
        self.nextDay_button = tk.Button(self.configureLF, text='create data', state='disabled', width=10, command=self.makeData)
        self.nextDay_button.place(x=120, y=300)
        
        #quit bottom
        self.close_button = tk.Button(self.master, text='CLOSE', width=10, font=('',10,'bold'), command=self.quit_app)
        self.close_button.grid(row=1, column=1, padx=20, sticky=tk.SE)

        self.master.protocol("WM_DELETE_WINDOW", self.quit_app)
        
    #inital ax
    def ax_configure(self):
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_xlim(0, 23)
        self.ax.set_ylim(0, 100)
        self.ax.set_xticks(np.arange(0,24,1))
        self.ax.set_yticks(np.arange(0,110,10))
        self.ax.grid(True)
        self.ax.set_xlabel("time(hour)")
        self.ax.set_ylabel("value(ml)")
        
    #choose the inputFolder
    def chooseFolder(self):
        self.folder_path.set(filedialog.askdirectory()) 
        if self.folder_path.get() and self.currentDate.get():
            self.nextDay_button['state'] = 'normal'
        else:
            self.nextDay_button['state'] = 'disabled'
    
    # set plot
    def showPlot(self, chooseBotton):
        self.fig.clf()
        self.ax_configure()
        if self.folder_path.get():
            if chooseBotton == 1:
                self.currentDate.set(self.calendar.get_date())
                self.ax.set_title('Line graph of ' + self.calendar.get_date())
                if os.path.exists(os.path.join(self.folder_path.get(), self.calendar.get_date()+'.csv')):
                    X_time = pd.read_csv(os.path.join(self.folder_path.get(), self.calendar.get_date()+'.csv'), header=None, skiprows=1, usecols=[0])
                    Y_data1 = pd.read_csv(os.path.join(self.folder_path.get(), self.calendar.get_date()+'.csv'), header=None, skiprows=1, usecols=[1])
                    Y_data2 = pd.read_csv(os.path.join(self.folder_path.get(), self.calendar.get_date()+'.csv'), header=None, skiprows=1, usecols=[2])
                    self.ax.plot(X_time, Y_data1, label=pd.read_csv(os.path.join(self.folder_path.get(), self.calendar.get_date()+'.csv')).columns[1])
                    self.ax.plot(X_time, Y_data2, label=pd.read_csv(os.path.join(self.folder_path.get(), self.calendar.get_date()+'.csv')).columns[2])
                    self.ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5,), borderaxespad=0, fontsize=7)
            else:
                self.ax.set_title('Line graph of ' + self.currentDate.get())
                if os.path.exists(os.path.join(self.folder_path.get(), self.currentDate.get()+'.csv')):
                    X_time = pd.read_csv(os.path.join(self.folder_path.get(), self.currentDate.get()+'.csv'), header=None, skiprows=1, usecols=[0])
                    Y_data1 = pd.read_csv(os.path.join(self.folder_path.get(), self.currentDate.get()+'.csv'), header=None, skiprows=1, usecols=[1])
                    Y_data2 = pd.read_csv(os.path.join(self.folder_path.get(), self.currentDate.get()+'.csv'), header=None, skiprows=1, usecols=[2])
                    self.ax.plot(X_time, Y_data1, label=pd.read_csv(os.path.join(self.folder_path.get(), self.currentDate.get()+'.csv')).columns[1])
                    self.ax.plot(X_time, Y_data2, label=pd.read_csv(os.path.join(self.folder_path.get(), self.currentDate.get()+'.csv')).columns[2])
                    self.ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5,), borderaxespad=0, fontsize=7)
            if self.currentDate.get():
                self.nextDay_button['state'] = 'normal'
            self.canvas.draw()
        else:
            messagebox.showinfo('warning', 'must choose the input folder')
    
    # move last/next day
    def moveDay(self, move):
        if self.folder_path.get() and self.currentDate.get():
            if move == -1:
                self.currentDate.set((datetime.datetime.strptime(self.currentDate.get(), '%Y%m%d') - datetime.timedelta(days=1)).strftime('%Y%m%d'))
            elif move == 1:
                self.currentDate.set((datetime.datetime.strptime(self.currentDate.get(), '%Y%m%d') + datetime.timedelta(days=1)).strftime('%Y%m%d'))
            self.showPlot(None)
            self.calendar.selection_set((datetime.datetime.strptime(self.currentDate.get(), '%Y%m%d')))
    
    #make new data 
    def makeData(self):
        if self.folder_path_entry.get():
            dataList = []
            dataList.append(['TIME', 'DATA_A', 'DATA_B'])
            for i in range(0,240,2):
                dataList.append([i/10, random.randint(0, 100), random.randint(0, 100)])   
            with open(os.path.join(self.folder_path_entry.get(), self.currentDate.get()+'.csv'), 'w') as f:
                writer = csv.writer(f)
                writer.writerows(dataList)
            f.close()
            messagebox.showinfo('info', 'Have made the data of '+self.currentDate.get())
            self.showPlot(1)
        else:
            messagebox.showinfo('warning', 'must choose the input folder')

    def quit_app(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = application(master=root)
    app.mainloop()
    app.quit()

if __name__ == "__main__":
    main()

