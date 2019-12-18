#Importing modules 
import sys
from importlist import *

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default
LARGE_FONT = ("Verdana", 12)

def update_figure(name,screen_width,screen_height):
        subprocess.call('convert /pi-wrf/Output/{}.png \
                         -resize {}x{} /pi-wrf/Output/{}.gif' \
                        .format(name,screen_width*.8,screen_height*.8,name), shell=True)
        photo=tk.PhotoImage(file="/pi-wrf/Output/{}.gif".format(name))
        image_display.config(image=photo)
        image_display.image=photo
        
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
        topbanner = tk.Label(frame1_topbanner,
                             text="Your Results", 
                             font=("Arial Bold",40),
                             bg=gui_color[1])
        topbanner.pack(fill=tk.X)
        
        #Creating Label & Blank Image and placing them in a frame
        global image_display
        subprocess.call('convert /pi-wrf/WRF_System/lib/{}.gif -resize {}x{} /pi-wrf/Output/{}.gif'\
                        .format(name,screenwidth*.8,screenheight*.8,name), 
                        shell=True)
        photo=tk.PhotoImage(file="/pi-wrf/Output/{}.gif".format(name))
        image_display=tk.Label(frame2_main_image,image=photo,height=screenheight*.8,width=screenwidth*.8)       
        image_display.image=photo
        image_display.pack(side=tk.TOP,expand=1)
        
        #Creating Back Button
        from Pages.start_page   import StartPage
        button1=tk.Button(frame3_low_nav_bar,
                          text="reset",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : controller.show_frame(StartPage))
        button1.pack(fill=tk.X,side=tk.LEFT)
        
        #Creating Button
        button2=tk.Button(frame3_low_nav_bar,
                          text="exit",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda: controller.quit_app())
        button2.pack(fill=tk.X,side=tk.RIGHT)


        #create high temp button
        button3=tk.Button(frame4_high_nav_bar,
                          text="Relative Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Your_Domain_Relative",screenwidth,screenheight)])
        button3.pack(fill=tk.X,side=tk.LEFT)

        button4=tk.Button(frame4_high_nav_bar,
                          text="Domain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Your_Domain",screenwidth,screenheight)])
        button4.pack(fill=tk.X,side=tk.LEFT)

        button5=tk.Button(frame4_high_nav_bar,
                          text="High Temperature",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("High_Temperature",screenwidth,screenheight)])
        button5.pack(fill=tk.X,side=tk.LEFT)
        

        button6=tk.Button(frame4_high_nav_bar,
                          text="Low Temperature",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Low_Temperature",screenwidth,screenheight)])
        button6.pack(fill=tk.X,side=tk.LEFT)
        

        button7=tk.Button(frame4_high_nav_bar,
                          text="Rain",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Total_Precip",screenwidth,screenheight)])
        button7.pack(fill=tk.X,side=tk.LEFT)

        button8=tk.Button(frame4_high_nav_bar,
                          text="Snow",
                          bg=gui_color[2],
                          activebackground=gui_color[3],
                          command=lambda : [update_figure("Snow_Depth",screenwidth,screenheight)])
        button8.pack(fill=tk.X,side=tk.LEFT)
        
