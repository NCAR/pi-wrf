#Importing modules 
import sys
from importlist import *

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default
LARGE_FONT = ("Verdana", 12)

def run_command(command):
    process=subprocess.Popen(command,stdout=PIPE,stderr=PIPE,shell=True)
    while True:
        output=process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            subprocess.call('/pi-wrf/WRF_System/lib/Run_WRF_GUI_NCL', shell=True)
            btn_run_model.config(state="disabled")            
            btn_view_output.config(text="View Output",
                                   bd=2,
                                   state="normal",
                                   bg=gui_color[4],
                                   activebackground=gui_color[5],
                                   font=("Arial Bold",16))
            btn_view_output.pack(fill=tk.X,side=tk.LEFT)
            exit_button.config(text="exit",
                               state="normal",
                               bg=gui_color[2]
                               ,activebackground=gui_color[3])
            exit_button.pack(fill=tk.X,side=tk.RIGHT)
            reset_button.config(text="reset",bg=gui_color[2],activebackground=gui_color[3])
            reset_button.pack(fill=tk.X,side=tk.LEFT)
            break
        if output:         
            txt.see(tk.END)
            txt.insert(tk.END, output)
            txt.update_idletasks()
    rc = process.poll()
    return rc

def putintext():
    txt.insert('1.0',run_command('/pi-wrf/Run_WRF_GUI'))
    
def reset():
    txt.delete('1.0',tk.END)
    btn_run_model.config(state="normal")
    btn_view_output.pack_forget()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        screenwidth=self.winfo_screenwidth()                         #get the current screen width
        screenheight=self.winfo_screenheight()                       #current height of screen 

        import Pages.page_four
        def retrieve_figure():
            subprocess.call('convert /pi-wrf/Output/Your_Domain_Relative.png -resize {}x{} ../../Output/Your_Domain_Relative.gif'\
                            .format(screenwidth*.8,screenheight*.8), 
                            shell=True)
            photo=tk.PhotoImage(file="/pi-wrf/Output/Your_Domain_Relative.gif")
            Pages.page_four.image_display.config(image=photo)
            Pages.page_four.image_display.image=photo
          
        frame1_topbanner=tk.Frame(self)
        frame1_topbanner.pack(side=tk.TOP,fill=tk.X)
        topbanner = tk.Label(frame1_topbanner,
                             text="Your Model Is Running",
                             font=("Arial Bold",40),
                             bg=gui_color[0],
                             foreground="white")
        topbanner.pack(fill=tk.X)
        
        global frame2_map
        frame2_map=tk.Frame(self)
        frame2_map.pack(fill=tk.X,expand=0)
        
        frame3_map=tk.Frame(self)
        frame3_map.pack(fill=tk.BOTH,expand=1)

        global txt
        txt=tk.Text(frame3_map)
        txt.pack(fill=tk.BOTH,expand=True)
        
        global btn_run_model
        btn_run_model=tk.Button(frame2_map,
                                text="Run Model",
                                font=("Arial Bold",16),
                                command=lambda :[putintext()])
        btn_run_model.pack(fill=tk.X,side=tk.LEFT)

        global btn_view_output
        btn_view_output=tk.Button(frame2_map,
                                  bd=0,
                                  state="normal",
                                  command=lambda :[retrieve_figure(),
                                                   controller.show_frame(Pages.page_four.FigurePage),
                                                   reset()])
        btn_view_output.pack(fill=tk.X,side=tk.LEFT)
        btn_view_output.pack_forget()
        
        global exit_button,reset_button
        frame4_low_nav_bar=tk.Frame(self,bg=gui_color[1])
        frame4_low_nav_bar.pack(fill=tk.X,side=tk.BOTTOM,expand=0)
        exit_button=tk.Button(frame4_low_nav_bar,
                              text="reset",
                              bg=gui_color[2],
                              activebackground=gui_color[3],
                              command=lambda: controller.quit_app())
        exit_button.pack_forget()
        from Pages.start_page   import StartPage
        reset_button=tk.Button(frame4_low_nav_bar,
                               bd=0,
                               state="normal",
                               command=lambda : controller.show_frame(StartPage))
        reset_button.pack_forget()


