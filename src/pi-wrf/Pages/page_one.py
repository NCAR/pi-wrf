#This script creates page two of the app. 

#Importing modules 
import sys
from importlist import *
from Pages.start_page  import StartPage
from Pages.page_two   import PageTwo
import subprocess
from datetime import date, datetime, timedelta

#Set Color Scheme and Font
gui_color=color_scheme(1)  # 1=default
LARGE_FONT = ("Verdana", 12)


# Creating arrays of time options for user
# Arrays are based on system time
current_time=datetime.utcnow()
current_time=current_time.replace(microsecond=0,second=0,minute=0)
if current_time.hour >= 0 and current_time.hour < 3:
        current_time=current_time-timedelta(days=1)
        current_time=current_time.replace(hour=18)
elif current_time.hour >= 3 and current_time.hour < 9:
    current_time=current_time.replace(hour=0)
elif current_time.hour >= 9 and current_time.hour < 15:
    current_time=current_time.replace(hour=6)
elif current_time.hour >=15 and current_time.hour < 21:
    current_time=current_time.replace(hour=12)
elif current_time.hour >=21:
    current_time=current_time.replace(hour=18)
time_interval=6
days_back=2.
days_ahead=3.

init_times=[0]*int(((24/6)*days_back+1))
end_times=[0]*int(((24/6)*days_ahead+1))

init_time_delta=timedelta(hours=-time_interval)
end_time_delta=timedelta(hours=time_interval)


init_times[0]=current_time
for i in range(1,len(init_times),1):
    init_times[i]=init_times[i-1]+init_time_delta

time_delta=timedelta(hours=6)
end_times[0]=current_time
for i in range(1,len(end_times),1):
    end_times[i]=end_times[i-1]+end_time_delta



###############################################
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])    

	# Function that accepts user's time input and writes them to 
	# the file 'RUN_WRF_GUI' & outputs the slected time to user
	# User's time gets reformatted to mm-dd-yyyy-hh
        def get_run_duration():
            user_start_selection=start_times.get('active')
            user_start_selection=(user_start_selection[5:7]+
                                  user_start_selection[7:10]+
                                  "-"+
                                  user_start_selection[:4]+
                                   "-"+
                                  user_start_selection[11:13])
            subprocess.call("sed -i /userstartdate=/c\\userstartdate='{}' ../../Run_WRF_GUI".format(user_start_selection),shell=True)
        
            user_end_selection=duration_times.get('active')
            user_end_selection=(user_end_selection[5:7]+
                                user_end_selection[7:10]+
                                "-"+
                                user_end_selection[:4]+
                                "-"+
                                user_end_selection[11:13])
            subprocess.call("sed -i /userenddate=/c\\userenddate='{}' ../../Run_WRF_GUI".format(user_end_selection),shell=True)
 
            
            user_duration=datetime.strptime(user_end_selection,"%m-%d-%Y-%H") - \
                          datetime.strptime(user_start_selection,"%m-%d-%Y-%H")
            
            if user_duration.total_seconds()/60/60 == 0.0:
                output=("Start and end time match. Please change times to continue.")
                domain_button.config(state='disabled')
            else:
                output=("The duration of your simulation is "+str(user_duration.days)+
                        " days and "+str(((user_duration.total_seconds()/60)/60)%24)+
                        " hours.\n Click 'Choose Domain' to continue or"+
                        " 'Reset Selection' to choose new times.") 
            return output

	# A function that resets the buttons to the default state
        def clear_time_menu():
            #start_times.selection_clear(0,last='none')
            #duration_times.selection_clear(0,last='none')
            confirm_button.config(state='normal')
            domain_button.config(state='disabled')
            clear_button.config(state='disabled')
            duration_text.config(text="")
            start_times.config(state='normal')
            duration_times.config(state='normal')
            start_times.selection_clear(0,tk.END)
            duration_times.selection_clear(0,tk.END)
           
 
       # Laying out frames for top_banner, listboxes, and buttons
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=10)
        self.grid_rowconfigure(2,weight=100)
        self.grid_rowconfigure(3,weight=100)
        self.grid_rowconfigure(4,weight=100)
        self.grid_rowconfigure(5,weight=0)
        self.grid_rowconfigure(6,weight=100)
        self.grid_columnconfigure(0,weight=4)
        self.grid_columnconfigure(1,weight=4)
        self.grid_columnconfigure(2,weight=2)

        
        # Top Banner 
        top_banner = tk.Label(self,
                       text="Choose Simulation Start/End",
                       font=("Arial Bold",40),
                       bg=gui_color[1],
                       foreground="white")
        top_banner.grid(column=0,row=0,
                        sticky='ewns',
                        columnspan=3)


        # Begin Time Listbox (listbox & two labels)
        init_time_lbl = tk.Label(self,
                                 text="Start Time",
                                 font=("Arial Bold", 30),
                                 bg=gui_color[0],
                                 foreground="white")
        init_time_lbl.grid(column=0,row=1,
                           sticky='s')
        
        start_times = tk.Listbox(self,
                                 selectmode="ACTIVE",
                                 font=("Arial Bold",25),
                                 highlightcolor=gui_color[3],
                                 selectbackground=gui_color[4],
                                 exportselection=0)
        for i in range(0,len(init_times),1):
            start_times.insert(i,init_times[i])
        start_times.grid(column=0,row=2,
                         rowspan=3,
                         sticky='ns')

        utc_indicator = tk.Label(self,
                                 text="Times are in UTC",
                                 font=("Arial Bold",10),
                                 bg=gui_color[0],
                                 foreground="white")
        utc_indicator.grid(column=0,row=5,
                           sticky='n')
                                   
           

        # End Time Listbox (listbox & two labels)
        end_time_lbl = tk.Label(self, 
                                 text="End Time",
                                 font=("Arial Bold", 30),
                                 bg=gui_color[0],
                                 foreground="white")
        end_time_lbl.grid(column=1,row=1,
                          sticky='s')

        duration_times = tk.Listbox(self,
                                    font=("Arial Bold",25),
                                    highlightcolor=gui_color[3],
                                    selectbackground=gui_color[4],
                                    exportselection=0)
        for i in range(0,len(end_times),1):
            duration_times.insert(i,end_times[i])
        duration_times.config(font=("Arial Bold",25))
        duration_times.grid(column=1,row=2,
                            rowspan=3,
                            sticky='ns')

        utc_indicator_2 = tk.Label(self,
                                 text="Times are in UTC",
                                 font=("Arial Bold",10),
                                 bg=gui_color[0],
                                 foreground="white")
        utc_indicator_2.grid(column=1,row=5,
                             sticky='n')
        
        # Buttons (creating buttons on right side of page)
        buttons_frame=tk.Frame(self,bg=gui_color[0])
        buttons_frame.grid(row=3,column=2,
                           sticky='ewns')
  
        home_button = tk.Button(buttons_frame,
                                      text="HOME",
                                      font=("Arial Bold",40),
                                      bg=gui_color[2],
                                      activebackground=gui_color[3],
                                      command=lambda :[clear_time_menu(), 
                                                       controller.show_frame(StartPage)])
        home_button.pack(fill='x')

        clear_button = tk.Button(buttons_frame,
                                      text="Reset Selection",
                                      font=("Arial Bold",40),
                                      bg=gui_color[2],
                                      state='disabled',
                                      activebackground=gui_color[3],
                                      command=lambda :clear_time_menu())
        clear_button.pack(fill='x')
                          
        confirm_button = tk.Button(buttons_frame,
                                      text="Confirm Selection",
                                      font=("Arial Bold",40),
                                      bg=gui_color[2],
                                      activebackground=gui_color[3],
                                      command=lambda : [clear_button.config(state='normal'),
                                                        domain_button.config(state='normal'),
                                                        confirm_button.config(state='disabled'),
                                                        start_times.config(state='disabled'),
                                                        duration_times.config(state='disabled'),
                                                        duration_text.config(text=(get_run_duration()))])

        confirm_button.pack(fill='x')

        domain_button = tk.Button(buttons_frame,
                                      text="Choose Domain",
                                      font=("Arial Bold",40),
                                      bg=gui_color[2],
                                      state='disabled',
                                      activebackground=gui_color[3],
                                      command=lambda :[clear_time_menu(), 
                                                       duration_text.config(text=""),
                                                       controller.show_frame(PageTwo)])
        domain_button.pack(fill='x')

        duration_text = tk.Label(self,
                       font=("Arial Bold",20),
                       bg=gui_color[0],
                       text="",
                       foreground="white")
        duration_text.grid(column=0,row=6,
                        sticky='ewns',
                        columnspan=2)


