#Importing modules
import os
import matplotlib
import subprocess
import glob

from PIL import Image, ImageTk

#import sys
import tkinter as tk
from color_schemes     import color_scheme
import warnings
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

#Set Color Scheme and Font
gui_color=color_scheme(1)                     #1=default


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

class ResizingLabel(tk.Label): #inherit from Label Class
    def __init__(self, parent, imagepath, *args, **kwargs): #takes image-path and resize image to label-size
        tk.Label.__init__(self, parent, *args, **kwargs)

        # Default configure settings (Label has no border)
        self.configure(bd=0)

        self.parent=parent
        self.parent.bind('<Configure>', self._resize_image)

        self.imagepath = imagepath
        self.image = Image.open(self.imagepath)
        self.img_copy= self.image.copy()
        
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background = tk.Label(self, image=self.background_image,bd=0)
        self.background.grid(row=0,column=0,sticky="NSEW")
        self.background.grid_rowconfigure(0,weight=1)
        self.background.grid_columnconfigure(0,weight=1)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = self.parent.winfo_width()
        new_height = self.parent.winfo_height()

        self.image = self.img_copy.resize((new_width, new_height))
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)   


 
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

        def get_filenames(PATH,filename,*args):
            """ a function that counts the number of files
            matching a string with wildcards          """
            filenames = sorted(glob.glob('{}{}'.format(PATH,filename)))
            return filenames 
        
        def destroy_widgets(frame):
            for widgets in frame.winfo_children():
                widgets.destroy()
        
        def create_gallery(filenames):
            destroy_widgets(sub_holder)
            buttons=[]
            for index in range(len(filenames)):
                if filenames[index] == '/pi-wrf/Output/low_temp.png':
                    min_t_btn=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="Low Temps",
                                      bg=gui_color[3],
                                      command=lambda i=index : change_image(filenames[i])))
                    buttons.append(min_t_btn)
                    buttons[index].pack(anchor=tk.CENTER,side=tk.LEFT)
                elif filenames[index] == '/pi-wrf/Output/max_temp.png':
                    max_t_btn=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="High Temps",
                                      bg=gui_color[3],
                                      command=lambda i=index : change_image(filenames[i])))
                    buttons.append(max_t_btn)
                    buttons[index].pack(anchor=tk.CENTER,side=tk.LEFT)
                    save_btn=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="Save Temps",
                                      bg=gui_color[3],
                                      command=lambda : [
                                      os.system('cp /pi-wrf/Output/*temp* /pi-wrf/Output/user_saved_files')]))
                    buttons.append(save_btn)
                    buttons[-1].pack(anchor=tk.CENTER,side=tk.LEFT)
                elif filenames[index] == ('/pi-wrf/Output/max_wind.png'):
                    button=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="Max Winds",
                                      bg=gui_color[3],
                                      command=lambda i=index : change_image(filenames[i])))
                    buttons.append(button)
                    save_btn=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="Save Temps",
                                      bg=gui_color[3],
                                      command=lambda : [
                                      os.system('cp /pi-wrf/Output/*wind* /pi-wrf/Output/user_saved_files')]))
                    buttons.append(save_btn)
                    buttons[index].pack(anchor=tk.CENTER,side=tk.LEFT)
                    buttons[-1].pack(anchor=tk.CENTER,side=tk.LEFT)
                elif filenames[index] == ('/pi-wrf/Output/rain_total.png'):
                    button=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="Total Rain",
                                      bg=gui_color[3],
                                      command=lambda i=index : change_image(filenames[i])))
                    buttons.append(button)
                    save_btn=(tk.Button(sub_holder,
                                       font=('Arial Bold',13),
                                       text="Save Rainfall",
                                       bg=gui_color[3],
                                       command=lambda : [
                                       os.system('cp /pi-wrf/Output/*rain* /pi-wrf/Output/user_saved_files')]))
                    buttons.append(save_btn)
                    buttons[index].pack(anchor=tk.CENTER,side=tk.LEFT)
                    buttons[-1].pack(anchor=tk.CENTER,side=tk.LEFT)
                elif filenames[index] == ('/pi-wrf/Output/snow_total.png'):
                    button=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="Total Snow",
                                      bg=gui_color[3],
                                      command=lambda i=index : change_image(filenames[i])))
                    buttons.append(button)
                    save_btn=(tk.Button(sub_holder,
                                       font=('Arial Bold',13),
                                       text="Save Snowfall",
                                       bg=gui_color[3],
                                       command=lambda : [
                                       os.system('cp /pi-wrf/Output/*snow* /pi-wrf/Output/user_saved_files')]))
                    buttons.append(save_btn)
                    buttons[index].pack(anchor=tk.CENTER,side=tk.LEFT)
                    buttons[-1].pack(anchor=tk.CENTER,side=tk.LEFT)
                else:
                    button=(tk.Button(sub_holder,
                                      font=('Arial Bold',13),
                                      text="{:02d}".format(index),
                                      bg=gui_color[3],
                                      command=lambda i=index : change_image(filenames[i])))
                    buttons.append(button)
                    buttons[index].pack(anchor=tk.CENTER,side=tk.LEFT)

        #Creating Frames
        frame1_topbanner=tk.Frame(self)
        frame1_topbanner.place(relx=0,rely=0,relwidth=1,relheight=.07)
        
        frame4_high_nav_bar=tk.Frame(self)
        frame4_high_nav_bar.place(relx=0,rely=.07,relwidth=1,relheigh=.03)
        holder=tk.Frame(frame4_high_nav_bar)
        holder.pack(expand=tk.TRUE)
        
        frame5_high_nav_sub_bar=tk.Frame(self)
        frame5_high_nav_sub_bar.place(relx=0,rely=.1,relwidth=1,relheight=.04)
        sub_holder=tk.Frame(frame5_high_nav_sub_bar)
        sub_holder.pack(expand=tk.TRUE)
        frame2_main_image=tk.Frame(self)
        frame2_main_image.place(relx=0,rely=.14,relwidth=1,relheight=.81)
        
        #frame2_main_image.pack_propagate(0)
        frame3_low_nav_bar=tk.Frame(self,bg=gui_color[1])
        frame3_low_nav_bar.place(relx=0,rely=.95,relwidth=1,relheight=.05)
        
        main_img_frame=tk.Frame(frame2_main_image)
        main_img_frame.place(relx=.25,rely=0,relwidth=.5,relheight=1)
        
        #Creating Top Banner
        topbanner_lbl = tk.Label(frame1_topbanner,
                             text="Your Results", 
                             font=('Arial Bold',40),
                             bg=gui_color[1])
        topbanner_lbl.pack(fill=tk.X,expand=1)

        def feature_img_change(image_path):
            global main_img
            try:
                main_img.forget()
            except:
                pass
            main_img = ResizingLabel(main_img_frame,image_path)

        def change_image(file):
            image_display.forget()
            feature_img_change(file),
            main_img.pack(fill='both')
            main_img.pack_propagate(1)
         
        #Creating Label & Blank Image and placing them in a frame
        global image_display
        photo=tk.PhotoImage()
        image_display=tk.Label(frame2_main_image,image=photo,height=screenheight*.8,width=screenwidth*.8)       
        image_display.image=photo
        image_display.pack(side=tk.TOP,expand=1)
        
        from Pages.start_page   import StartPage
        reset_btn=tk.Button(frame3_low_nav_bar,
                          text="RESET",
                          bg=gui_color[2],
                          font=('Arial Bold',20),
                          activebackground=gui_color[3],
                          command=lambda : [controller.show_frame(StartPage),
                                            main_img.forget(),
                                            destroy_widgets(sub_holder)])
        reset_btn.pack(fill=tk.X,side=tk.LEFT)
        
        exit_btn=tk.Button(frame3_low_nav_bar,
                          text="EXIT",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          font=('Arial Bold',20),
                          command=lambda: controller.quit_app())
        exit_btn.pack(fill=tk.X,side=tk.RIGHT)

        rel_dom_btn=tk.Button(holder,
                          text="Relative Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [create_gallery(get_filenames(None,None)),
                                            change_image('/pi-wrf/Output/Your_Domain_Relative.png')])
        rel_dom_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER)

        abs_dom_btn=tk.Button(holder,
                          text="Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [create_gallery(get_filenames(None,None)),
                                            change_image('/pi-wrf/Output/Your_Domain.png')])
        abs_dom_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER)

        high_temp_btn=tk.Button(holder,
                          text="Temperature",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [create_gallery(get_filenames('/pi-wrf/Output/','*temp*')),
                                            change_image('/pi-wrf/Output/hourly-temperature_00.png')])
        high_temp_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER)

        wind_btn=tk.Button(holder,
                          text="Wind",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [create_gallery(get_filenames('/pi-wrf/Output/','*wind*')),
                                            change_image('/pi-wrf/Output/hourly-wind_00.png')])
        wind_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER)


        rain_btn=tk.Button(holder,
                          text="Rain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [create_gallery(get_filenames('/pi-wrf/Output/','*rain*')),
                                            change_image('/pi-wrf/Output/hourly_rain_00.png')])
        rain_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER)

        snow_btn=tk.Button(holder,
                          text="Snow",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [create_gallery(get_filenames('/pi-wrf/Output/','*snow*')),
                                            change_image('/pi-wrf/Output/hourly_snow_00.png')])
        snow_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER)
       
        save_btn=tk.Button(holder,
			   text="Save All Figures",
			   bg=gui_color[2],
			   activebackground=gui_color[3],
			   command=lambda : [save_output(),
                                tk.messagebox.showinfo("Output Saved",
                                                       "Figures were saved to your local directory")])
        save_btn.pack(fill=tk.X,side=tk.LEFT,anchor=tk.CENTER) 
