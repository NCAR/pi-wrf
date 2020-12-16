#Importing standard modules
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

#importing local modules
from color_schemes     import color_scheme

#Set Color Scheme and Font
gui_color=color_scheme(1)                                            # 1=default


def run_command(command):
    """ runs the WRF model, pipes command prompt output to a frame within the
    main window, and manages the state of buttons in the top nav bar on the page"""
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    while True:
        output=process.stdout.readline().decode()
        if output == '' and process.poll() is not None:
            run_model_btn.config(state='disabled')
            save_exec_output_btn.pack(fill=tk.X,side=tk.LEFT)
            view_output_btn.config(text="View Output",
                                   bd=2,
                                   state='normal',
                                   bg=gui_color[4],
                                   activebackground=gui_color[5],
                                   font=('Arial Bold',16))
            view_output_btn.pack(fill=tk.X,side=tk.LEFT)


            exit_btn.config(text="exit",
                            state='normal',
                            bg=gui_color[2],
                            activebackground=gui_color[3])
            exit_btn.pack(fill=tk.X,side=tk.RIGHT)
            reset_btn.config(text='reset',
                             bg=gui_color[2],
                            activebackground=gui_color[3])
            reset_btn.pack(fill=tk.X,side=tk.LEFT)
            break
        
        if output:
            txt.see(tk.END)
            txt.insert(tk.END, output)
            txt.update_idletasks()
    
    rc = process.poll()
    return rc

def putintext():
    """ inserts the command prompt text into a frame within the main window"""
    txt.insert('1.0',run_command('/pi-wrf/run_wrf'))

def save_exec_output():
    """saves the command prompt output to a user-mounted directory"""
    os.system('cp /pi-wrf/Output/*exec* /pi-wrf/Output/user_saved_files')
    
def reset():
    """ resets the page by clearing buttons and removing all displayed command prompt text"""
    txt.delete('1.0',tk.END)
    run_model_btn.config(state='normal')
    view_output_btn.pack_forget()
    save_exec_output_btn.pack_forget()

class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        screenwidth=self.winfo_screenwidth()     #get the current screen width
        screenheight=self.winfo_screenheight()   #current height of screen

        import Pages.page_four
        def retrieve_figure():
            """ grabs a figure and caches it within the next page """
            subprocess.call('convert /pi-wrf/Output/Your_Domain_Relative.png '
                            '-resize {}x{} ../../Output/Your_Domain_Relative.gif'\
                            .format(screenwidth*.8,screenheight*.8),shell=True)
            photo=tk.PhotoImage(file="/pi-wrf/Output/Your_Domain_Relative.gif")
            Pages.page_four.image_display.config(image=photo)
            Pages.page_four.image_display.image=photo
          
        frame1_topbanner=tk.Frame(self)
        frame1_topbanner.pack(side=tk.TOP,fill=tk.X)
        topbanner_lbl = tk.Label(frame1_topbanner,
                             text="Start Your Simulation",
                             font=('Arial Bold',40),
                             bg=gui_color[0],
                             foreground='white')
        topbanner_lbl.pack(fill=tk.X)
        
        global frame2_map
        frame2_map=tk.Frame(self)
        frame2_map.pack(fill=tk.X,expand=0)
        
        frame3_map=tk.Frame(self)
        frame3_map.pack(fill=tk.BOTH,expand=1)

        global txt
        txt=tk.Text(frame3_map)
        txt.pack(fill=tk.BOTH,expand=True)
        
        global run_model_btn
        run_model_btn=tk.Button(frame2_map,
                                text="Run Model",
                                font=('Arial Bold',16),
                                command=lambda :[topbanner_lbl.config(text="Your Simulation is Running"),
                                putintext(),
                                topbanner_lbl.config(text="Your Simulation has Finished")])
        run_model_btn.pack(fill=tk.X,side=tk.LEFT)

        global view_output_btn, save_exec_output_btn
        save_exec_output_btn=tk.Button(frame2_map,
                                       text="Save Output Text",
                                       bd=2,
                                       state='normal',
                                       bg=gui_color[2],
                                       activebackground=gui_color[3],
                                       font=('Arial Bold',16),
                                       command=lambda: [save_exec_output(),
                                                        messagebox.showinfo("Output Saved",
                                                        "Text output was saved to your local directory")])
        save_exec_output_btn.pack(fill=tk.X,side=tk.LEFT)
        save_exec_output_btn.pack_forget()

        view_output_btn=tk.Button(frame2_map,
                                  bd=0,
                                  state='normal',
                                  command=lambda :[retrieve_figure(),
						   topbanner_lbl.config(text="Start Your Simulation"),
                                                   controller.show_frame(Pages.page_four.FigurePage),
                                                   reset(),
						   reset_btn.pack_forget(),
                                                   exit_btn.pack_forget()])
        view_output_btn.pack(fill=tk.X,side=tk.LEFT)
        view_output_btn.pack_forget()
                        
        global exit_btn,reset_btn
        frame4_low_nav_bar=tk.Frame(self,bg=gui_color[1])
        frame4_low_nav_bar.pack(fill=tk.X,side=tk.BOTTOM,expand=0)
        
        exit_btn=tk.Button(frame4_low_nav_bar,
                           text="reset",
                           bg=gui_color[2],
                           activebackground=gui_color[3],
                           command=lambda: controller.quit_app())
        exit_btn.pack_forget()
        
        from Pages.start_page   import StartPage
        reset_btn=tk.Button(frame4_low_nav_bar,
                               bd=0,
                               state='normal',
                               command=lambda : [topbanner_lbl.config(text="Start Your Simulation"),
						                      reset(),
                                                                      save_exec_output_btn.pack_forget(),
						                      reset_btn.pack_forget(),
                                                                      exit_btn.pack_forget(),
                                                                      controller.show_frame(StartPage)])
        
