# importing standard modules 
import datetime
import subprocess
import tkinter as tk

# import local modules
from color_schemes     import color_scheme

# set gui color scheme
gui_color=color_scheme(1)  # 1=default

current_time=datetime.datetime.utcnow().replace(microsecond=0,
                                                second=0,
                                                minute=0)

# rounding current hour to appropriate 6th hour for GFS initital conditions
if current_time.hour >= 0 and current_time.hour < 3:
    current_time=current_time-datetime.timedelta(days=1).replace(hour=18)
elif current_time.hour >= 3 and current_time.hour < 9:
    current_time=current_time.replace(hour=0)
elif current_time.hour >= 9 and current_time.hour < 15:
    current_time=current_time.replace(hour=6)
elif current_time.hour >=15 and current_time.hour < 21:
    current_time=current_time.replace(hour=12)
elif current_time.hour >=21:
    current_time=current_time.replace(hour=18)

# range and interval of start dates and end dates
time_interval=6
days_back=2
days_ahead=3

init_times=[0]*int(((24/6)*days_back+1))
end_times=[0]*int(((24/6)*days_ahead+1))

init_time_delta=datetime.timedelta(hours=-time_interval)
end_time_delta=datetime.timedelta(hours=time_interval)

init_times[0]=current_time
for i in range(1,len(init_times),1):
    init_times[i]=init_times[i-1]+init_time_delta

time_delta=datetime.timedelta(hours=6)
end_times[0]=current_time
for i in range(1,len(end_times),1):
    end_times[i]=end_times[i-1]+end_time_delta


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])

        def get_run_duration():
            """Function that accepts user's time input and writes them to 
            the file 'RUN_WRF_GUI' & outputs the slected time to user
            User's time gets reformatted to mm-dd-yyyy-hh"""
            user_start_selection=start_times_lbx.get('active')
            user_start_selection=(user_start_selection[5:7]+
                                  user_start_selection[7:10]+
                                  '-'+
                                  user_start_selection[:4]+
                                   '-'+
                                  user_start_selection[11:13])
            subprocess.call('sed -i /userstartdate=/c\\userstartdate="{}" '
                            ' /pi-wrf/run_wrf'.format(user_start_selection),shell=True)
        
            user_end_selection=duration_times_lbx.get('active')
            user_end_selection=(user_end_selection[5:7]+
                                user_end_selection[7:10]+
                                '-'+
                                user_end_selection[:4]+
                                '-'+
                                user_end_selection[11:13])
            subprocess.call('sed -i /userenddate=/c\\userenddate="{}" '
                            '/pi-wrf/run_wrf'.format(user_end_selection),shell=True)

            user_duration=datetime.datetime.strptime(user_end_selection,'%m-%d-%Y-%H') - \
                          datetime.datetime.strptime(user_start_selection,'%m-%d-%Y-%H')
            
            if user_duration.total_seconds()/60/60 == 0.0:
                output=('Start and end time match. Please change times to continue.')
                domain_btn.config(state='disabled')
            else:
                output=('The duration of your simulation is '+str(user_duration.days)+
                        ' days and '+str(((user_duration.total_seconds()/60)/60)%24)+
                        ' hours.\n Click "Choose Domain" to continue or'+
                        ' "Reset Selection" to choose new times.') 
            return output

        def clear_time_menu():
            """ A method that resets the buttons to
            the default state """
            confirm_btn.config(state='normal')
            domain_btn.config(state='disabled')
            clear_btn.config(state='disabled')
            duration_text_lbl.config(text='')
            start_times_lbx.config(state='normal')
            duration_times_lbx.config(state='normal')
            start_times_lbx.selection_clear(0,tk.END)
            duration_times_lbx.selection_clear(0,tk.END)
 
        # laying out frames for top_banner, listboxes, and buttons
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

        # banners, listboxes, labels, buttons
        top_banner_lbl = tk.Label(self,
                                  text='Choose Simulation Start/End',
                                  font=('Arial Bold',40),
                                  bg=gui_color[1],
                                  foreground='white')
        top_banner_lbl.grid(column=0,
                            row=0,
                            sticky='ewns',
                            columnspan=3)

        init_time_lbl = tk.Label(self,
                                 text='Start Time',
                                 font=('Arial Bold', 30),
                                 bg=gui_color[0],
                                 foreground='white')
        init_time_lbl.grid(column=0,
                           row=1,
                           sticky='s')
        
        start_times_lbx = tk.Listbox(self,
                                     selectmode='ACTIVE',
                                     font=('Arial Bold',25),
                                     highlightcolor=gui_color[3],
                                     selectbackground=gui_color[4],
                                     exportselection=0)
        start_times_lbx.grid(column=0,
                             row=2,
                             rowspan=3,
                             sticky='ns')
        for i in range(0,len(init_times),1):
            start_times_lbx.insert(i,init_times[i])
        
        utc_indicator_lbl = tk.Label(self,
                                     text='Times are in UTC',
                                     font=('Arial Bold',10),
                                     bg=gui_color[0],
                                     foreground='white')
        utc_indicator_lbl.grid(column=0,
                               row=5,
                               sticky='n')

        end_time_lbl = tk.Label(self, 
                                 text='End Time',
                                 font=('Arial Bold', 30),
                                 bg=gui_color[0],
                                 foreground='white')
        end_time_lbl.grid(column=1,
                          row=1,
                          sticky='s')

        duration_times_lbx = tk.Listbox(self,
                                        font=('Arial Bold',25),
                                        highlightcolor=gui_color[3],
                                        selectbackground=gui_color[4],
                                        exportselection=0)
        duration_times_lbx.config(font=('Arial Bold',25))
        duration_times_lbx.grid(column=1,
                                row=2,
                                rowspan=3,
                                sticky='ns')
        for i in range(0,len(end_times),1):
            duration_times_lbx.insert(i,end_times[i])

        utc_indicator_2_lbl = tk.Label(self,
                                 text='Times are in UTC',
                                 font=('Arial Bold',10),
                                 bg=gui_color[0],
                                 foreground='white')
        utc_indicator_2_lbl.grid(column=1,
                                 row=5,
                                 sticky='n')
        
        buttons_frame=tk.Frame(self,bg=gui_color[0])
        buttons_frame.grid(row=3,
                           column=2,
                           sticky='ewns')
  
        from Pages.start_page  import StartPage
        home_btn = tk.Button(buttons_frame,
                             text='HOME',
                             font=('Arial Bold',40),
                             bg=gui_color[2],
                             activebackground=gui_color[3],
                             command=lambda :[clear_time_menu(), 
                                              controller.show_frame(StartPage)])
        home_btn.pack(fill='x')

        clear_btn = tk.Button(buttons_frame,
                              text='Reset Selection',
                              font=('Arial Bold',40),
                              bg=gui_color[2],
                              state='disabled',
                              activebackground=gui_color[3],
                              command=lambda :clear_time_menu())
        clear_btn.pack(fill='x')
                          
        confirm_btn = tk.Button(buttons_frame,
                                text='Confirm Selection',
                                font=('Arial Bold',40),
                                bg=gui_color[2],
                                activebackground=gui_color[3],
                                command=lambda : [clear_btn.config(state='normal'),
                                                  domain_btn.config(state='normal'),
                                                  confirm_btn.config(state='disabled'),
                                                  start_times_lbx.config(state='disabled'),
                                                  duration_times_lbx.config(state='disabled'),
                                                  duration_text_lbl.config(text=(get_run_duration()))])
        confirm_btn.pack(fill='x')

        from Pages.page_two   import PageTwo
        domain_btn = tk.Button(buttons_frame,
                               text='Choose Domain',
                               font=('Arial Bold',40),
                               bg=gui_color[2],
                               state='disabled',
                               activebackground=gui_color[3],
                               command=lambda :[clear_time_menu(), 
                                                duration_text_lbl.config(text=''),
                                                controller.show_frame(PageTwo)])
        domain_btn.pack(fill='x')

        duration_text_lbl = tk.Label(self,
                                     font=('Arial Bold',20),
                                     bg=gui_color[0],
                                     text='',
                                     foreground='white')
        duration_text_lbl.grid(column=0,
                               row=6,
                               sticky='ewns',
                               columnspan=2)


