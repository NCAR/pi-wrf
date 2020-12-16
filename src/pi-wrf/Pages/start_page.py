# importing standard modules 
import requests
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# set color scheme and font
from color_schemes     import color_scheme
gui_color=color_scheme(1)      # 1=default

def check_internet():
    url='https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs'
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
        self.image = Image.open("/pi-wrf/WRF_System/lib/start_page_bg.jpg")
        self.background_image = ImageTk.PhotoImage(self.image)
        
        # configuring layout of widgets
        self.grid_columnconfigure(0,weight=4)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=3)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=3)
        self.grid_rowconfigure(4,weight=1)
        
        # background label
        bg_lbl = tk.Label(self,image=self.background_image)
        bg_lbl.image = self.background_image
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
            run_fcst_btn.config(command=lambda : [messagebox.showerror('Warning', 
                                                  'No network connection detected or no access to the NCEP Server.\n\n'
                                                  'Unable to retrieve initial conditions and run live simulations. ' 
                                                  'Please exit the application and check network connection.\n\n'
                                                  'If network connection is established check the NCEP server:\n\n'
                                                  'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs\n\n'
                                                  'If the server is down, wait a few hours as the server undergoes maintenance.' )])    
        
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
                                 text=('Pi-WRF Version 2.00.01'),
                                 anchor='w',
                                 font=('Arial Bold',5),
                                 fg='black',
                                 bg=gui_color[1])
        version_lbl.grid(row=4,sticky='sew')
