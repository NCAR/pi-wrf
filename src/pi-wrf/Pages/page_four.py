#Importing modules
import os
import matplotlib
import subprocess

#import sys
import tkinter as tk
from color_schemes     import color_scheme
import warnings
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)
#from importlist import *



#Set Color Scheme and Font
gui_color=color_scheme(1)                     #1=default
#LARGE_FONT = ("Verdana", 12)

def update_figure(name,screen_width,screen_height):
        subprocess.call('convert /pi-wrf/Output/{}.png \
                         -resize {}x{} /pi-wrf/Output/{}.gif' \
                        .format(name,screen_width*.8,screen_height*.8,name),
                        shell=True)
        photo=tk.PhotoImage(file="/pi-wrf/Output/{}.gif".format(name))
        image_display.config(image=photo)
        image_display.image=photo

def save_output():
    os.system('cp /pi-wrf/Output/*.png /pi-wrf/Output/user_saved_files')
    
        
class FigurePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])
        screenwidth=self.winfo_screenwidth()                         #get the current screen width
        screenheight=self.winfo_screenheight()                       #current height of screen 

        #Setting Variables
        global image_display
        global frame2_main_image
        name="dummy_image"
        
                
        #Creating Frames
        frame1_topbanner=tk.Frame(self)
        frame1_topbanner.pack(side=tk.TOP,fill=tk.X)
        frame4_high_nav_bar=tk.Frame(self)
        frame4_high_nav_bar.pack(side=tk.TOP)
        frame2_main_image=tk.Frame(self)
        frame2_main_image.pack(fill=tk.BOTH,expand=1) 
        frame3_low_nav_bar=tk.Frame(self,bg=gui_color[1])
        frame3_low_nav_bar.pack(fill=tk.X,side=tk.BOTTOM,expand=0)
        
        #Creating Top Banner
        topbanner_lbl = tk.Label(frame1_topbanner,
                             text="Your Results", 
                             font=('Arial Bold',40),
                             bg=gui_color[1])
        topbanner_lbl.pack(fill=tk.X)
        
        #Creating Label & Blank Image and placing them in a frame
        global image_display
        subprocess.call('convert /pi-wrf/WRF_System/lib/{}.gif -resize {}x{} /pi-wrf/Output/{}.gif'\
                        .format(name,screenwidth*.8,screenheight*.8,name), 
                        shell=True)
        photo=tk.PhotoImage(file='/pi-wrf/Output/{}.gif'.format(name))
        image_display=tk.Label(frame2_main_image,image=photo,height=screenheight*.8,width=screenwidth*.8)       
        image_display.image=photo
        image_display.pack(side=tk.TOP,expand=1)
        
        from Pages.start_page   import StartPage
        reset_btn=tk.Button(frame3_low_nav_bar,
                          text="reset",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : controller.show_frame(StartPage))
        reset_btn.pack(fill=tk.X,side=tk.LEFT)
        
        exit_btn=tk.Button(frame3_low_nav_bar,
                          text="exit",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda: controller.quit_app())
        exit_btn.pack(fill=tk.X,side=tk.RIGHT)

        rel_dom_btn=tk.Button(frame4_high_nav_bar,
                          text="Relative Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Your_Domain_Relative",screenwidth,screenheight)])
        rel_dom_btn.pack(fill=tk.X,side=tk.LEFT)

        abs_dom_btn=tk.Button(frame4_high_nav_bar,
                          text="Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Your_Domain",screenwidth,screenheight)])
        abs_dom_btn.pack(fill=tk.X,side=tk.LEFT)

        high_temp_btn=tk.Button(frame4_high_nav_bar,
                          text="High Temperature",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("High_Temperature",screenwidth,screenheight)])
        high_temp_btn.pack(fill=tk.X,side=tk.LEFT)
        

        low_temp_btn=tk.Button(frame4_high_nav_bar,
                          text="Low Temperature",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Low_Temperature",screenwidth,screenheight)])
        low_temp_btn.pack(fill=tk.X,side=tk.LEFT)
        

        wind_btn=tk.Button(frame4_high_nav_bar,
                          text="Wind",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Surface_Wind",screenwidth,screenheight)])
        wind_btn.pack(fill=tk.X,side=tk.LEFT)


        rain_btn=tk.Button(frame4_high_nav_bar,
                          text="Rain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Total_Precip",screenwidth,screenheight)])
        rain_btn.pack(fill=tk.X,side=tk.LEFT)

        snow_btn=tk.Button(frame4_high_nav_bar,
                          text="Snow",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Snow_Depth",screenwidth,screenheight)])
        snow_btn.pack(fill=tk.X,side=tk.LEFT)
       
        save_btn=tk.Button(frame4_high_nav_bar,
			   text="Save Figures",
			   bg=gui_color[2],
			   activebackground=gui_color[3],
			   command=lambda : [save_output(),
                                tk.messagebox.showinfo("Output Saved",
                                                       "Figures were saved to your local directory")])
        save_btn.pack(fill=tk.X,side=tk.LEFT) 
