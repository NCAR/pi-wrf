#Importing modules 
import sys
from importlist import *
import requests
from tkinter import messagebox

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default
LARGE_FONT = ("Verdana", 12)

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])
        screenwidth=self.winfo_screenwidth()                         #get the current screen width
        screenheight=self.winfo_screenheight()                       #current height of screen
        subprocess.call('convert /pi-wrf/WRF_System/lib/start_page_bg.jpg -resize {}x{}\! /pi-wrf/WRF_System/lib/start_page_bg.gif'\
                        .format(screenwidth,screenheight),
                        shell=True)
        photo=tk.PhotoImage(file="/pi-wrf/WRF_System/lib/start_page_bg.gif")
        self.grid_columnconfigure(0,weight=4)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=3)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=3)
        self.grid_rowconfigure(4,weight=1)
        bg_label_test=tk.Label(self,image=photo)
        bg_label_test.image=photo
        bg_label_test.place(x=0,y=0,relwidth=1,relheight=1)

        topbanner = tk.Label(self,
                             bg=gui_color[1],
                             font=("Arial Bold",40),
                             text="Welcome to the Raspberry Pi-WRF Application")
        topbanner.grid(column=0,columnspan=3,sticky='new')
        
        from Pages.page_one   import PageOne
        btn_1 = tk.Button(self,
                          text="Run Forecast",
                          font=("Arial Bold",40),
                          borderwidth=5,bg=gui_color[2],
                          activebackground=gui_color[3],
                          width=20,
                          command=lambda : [controller.show_frame(PageOne),check_internet()])
        btn_1.grid(row=1,sticky='s') 
        if check_internet():
            btn_1.config(command=lambda : [controller.show_frame(PageOne)])
        else:
            btn_1.config(command=lambda : [messagebox.showwarning("Warning", "No network connection detected. cannot run live simulation. Please exit application and check connection.")])                      
        btn_2 = tk.Button(self,
                          text="Run Archived Simulation",
                          font=("Arial Bold",40),
                          borderwidth=5,
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          width=20,
                          command=lambda : messagebox.showwarning("Warning", 
                                                                   "Archived Simulations Are Not Yet Available"))
        btn_2.grid(row=2)
        btn_3 = tk.Button(self,
                          text="Exit",
                          font=("Arial Bold",40),
                          borderwidth=5,bg=gui_color[2],
                          activebackground=gui_color[3],
                          width=20,
                          command=lambda : controller.quit_app())
        btn_3.grid(row=3,sticky='n')

        version_lable = tk.Label(self,
                                 text=("Pi-WRF Version 1.2.0"),
                                 anchor="w",
                                 font=("Arial Bold",5),
                                 fg="black",
                                 bg=gui_color[1])
        version_lable.grid(row=4,sticky='sew')
