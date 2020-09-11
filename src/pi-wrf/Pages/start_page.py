# importing standard modules 
import requests
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox

# set color scheme and font
from color_schemes     import color_scheme
gui_color=color_scheme(1)                                            # 1=default

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
        subprocess.call('convert /pi-wrf/WRF_System/lib/start_page_bg.jpg -resize {}x{}\! '
                        ' /pi-wrf/WRF_System/lib/start_page_bg.gif'\
                        .format(screenwidth,screenheight),
                        shell=True)
        photo=tk.PhotoImage(file='/pi-wrf/WRF_System/lib/start_page_bg.gif')

        # configuring layout of widgets
        self.grid_columnconfigure(0,weight=4)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=3)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=3)
        self.grid_rowconfigure(4,weight=1)
        
        # background label
        bg_lbl = tk.Label(self,image=photo)
        bg_lbl.image = photo
        bg_lbl.place(x=0,y=0,relwidth=1,relheight=1)

        # header label
        header_lbl = tk.Label(self,
                              bg=gui_color[1],
                              font=('Arial Bold',40),
                              text='Welcome to the Raspberry Pi-WRF Application')
        header_lbl.grid(column=0,columnspan=3,sticky='new')
        
        # run forecast button
        from Pages.page_one  import PageOne #located here to prevent circular imports
        run_fcst_btn = tk.Button(self,
                                 text='Run Forecast',
                                 font=('Arial Bold',40),
                                 borderwidth=5,bg=gui_color[2],
                                 activebackground=gui_color[3],
                                 width=20,
                                 command=lambda : [controller.show_frame(PageOne),check_internet()])
        run_fcst_btn.grid(row=1,sticky='s') 
        if check_internet():
            run_fcst_btn.config(command=lambda : [controller.show_frame(PageOne)])
        else:
            run_fcst_btn.config(command=lambda : [messagebox.showwarning('Warning', 'No network connection detected. '
                                                 'cannot run live simulation. Please exit application and check connection.')])
        # archived sim button
        arc_sim_btn = tk.Button(self,
                          text='Run Archived Simulation',
                          font=('Arial Bold',40),
                          borderwidth=5,
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          width=20,
                          command=lambda : tk.messagebox.showwarning('Warning', 
                                                                  'Archived Simulations Are Not Yet Available'))
        arc_sim_btn.grid(row=2)
        
        # exit button
        exit_btn = tk.Button(self,
                          text='Exit',
                          font=('Arial Bold',40),
                          borderwidth=5,bg=gui_color[2],
                          activebackground=gui_color[3],
                          width=20,
                          command=lambda : controller.quit_app())
        exit_btn.grid(row=3,sticky='n')

        # version label
        version_lbl = tk.Label(self,
                                 text=('Pi-WRF Version 1.2.0'),
                                 anchor='w',
                                 font=('Arial Bold',5),
                                 fg='black',
                                 bg=gui_color[1])
        version_lbl.grid(row=4,sticky='sew')
