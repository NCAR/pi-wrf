#Importing standard modules 
import subprocess
import sys
import tkinter as tk

#Importin local modules
from color_schemes      import color_scheme
from Pages.start_page   import StartPage

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default


class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])
        screenwidth=self.winfo_screenwidth()                         #get the current screen width
        screenheight=self.winfo_screenheight()                       #current height of screen
  
        subprocess.call('convert /pi-wrf/WRF_System/lib/logo_splash_image.jpg -resize {}x{}\! /pi-wrf/WRF_System/lib/logo_splash_image.gif'\
                        .format(screenwidth,screenheight),
                        shell=True)
        bg = tk.PhotoImage(file="/pi-wrf/WRF_System/lib/logo_splash_image.gif")
        logo_bg = tk.Label(self,image=bg) 
        logo_bg.image = bg
        logo_bg.place(x=0,y=0,relwidth=1,relheight=1)


        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=1)

                
        continue_btn = tk.Button(self,
                          text="Continue",
                          font=("Arial Bold",40),
                          borderwidth=5,bg="white",
                          activebackground=gui_color[2],
                          width=10,
                          command=lambda : controller.show_frame(StartPage))
        continue_btn.grid(row=1, column=0)
        #continue_btn.place(anchor='s')
