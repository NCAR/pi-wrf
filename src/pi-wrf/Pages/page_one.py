#Importing modules 
import sys
from importlist import *

#Set Color Scheme and Font
gui_color=color_scheme(1)  # 1=default
LARGE_FONT = ("Verdana", 12)

#Setting Time and Date Options
months=['January','February','March','April','May','June','July','August','September','October','November','December']
days_in_month = [[31,28,31,30,31,30,31,31,30,31,30,31],
                [31,29,31,30,31,30,31,31,30,31,30,31]]
currenthour   = dt.datetime.utcnow().hour
currentmonth  = dt.datetime.now().month
currentday    = dt.datetime.now().day
currentyear   = dt.datetime.now().year

user_startdate_range=[currentday-5,currentday]
user_enddate_range=[currentday,currentday+14]

############################################################################
############################################################################
#If current day is at beginning of month ajust settings to go back one month
if currentday <= 5:
    user_startdate_range=[1,currentday]
    if currentmonth==1:
        months=[months[11],months[0]]
        days_in_month=[days_in_month[1][11],days_in_month[1][0]]
    elif currentmonth==3:
        months=[months[1],months[2]]
        if currentyear%4 == 0:
            days_in_month=[days_in_month[1][1],days_in_month[1][2]]
        else:
            days_in_month=[days_in_month[0][1],days_in_month[0][2]]
    else:
        months=[months[currentmonth-2],months[currentmonth-1]]
        days_in_month=[days_in_month[0][currentmonth-2],days_in_month[0][currentmonth-1]]

#Settings if current day is in middle of month
if (currentday > 5) and (currentday < 15):
    user_enddate_range=[currentday,currentday+14]    
    months=[months[currentmonth-1]]
    days_in_month=[days_in_month[0][currentmonth-1]]

#Settings if current day is at end of month
if currentday >= 15:
    if currentmonth==2:
        months=[months[1],months[2]]
        if currentyear%4 == 0:
            days_in_month=[days_in_month[1][1],days_in_month[1][2]]
            user_enddate_range=[currentday,days_in_month[0]]
        else:
            days_in_month=[days_in_month[0][1],days_in_month[0][2]]
            user_enddate_range=[currentday,days_in_month[0]]
    elif currentmonth==12:
        months=[months[11],months[0]]
        days_in_month=[days_in_month[0][11],days_in_month[0][0]]
        user_enddate_range=[currentday,days_in_month[0]]
    else:
        months=[months[currentmonth-1],months[currentmonth]]
        days_in_month=[days_in_month[0][currentmonth-1],days_in_month[0][currentmonth]]
        user_enddate_range=[currentday,days_in_month[0]]

#Map current time to zulu time            
if (currenthour >= 3) and (currenthour < 9):
    forecasthour=00
elif (currenthour >= 9) and (currenthour < 15):
    forecasthour=6
elif (currenthour >= 15) and (currenthour < 21):
    forecasthour=12
elif (currenthour >= 21) or (currenthour < 3):
    forecasthour=18


def update_spinbox_start(sb_start_month):
    heresavalue=sb_start_month.get()    
    if currentday <= 5:
        if heresavalue==months[0]:
            sb_start_day.delete(0,'end')
            sb_start_day.insert(0,days_in_month[0])
            sb_start_day.config(from_=(days_in_month[0]-(5-currentday)),to=days_in_month[0])
            
        elif heresavalue==months[1]:
            sb_start_day.delete(0,'end')
            sb_start_day.insert(0,currentday)
            sb_start_day.config(from_=1,to=currentday)
           
def update_spinbox_end():
    heresavalue_b=sb_end_month.get()
    if currentday >=15:
        if heresavalue_b==months[0]:
            sb_end_day.delete(0,'end')
            sb_end_day.insert(0,currentday+1)
            sb_end_day.config(from_=currentday,to=days_in_month[0])
            if heresavalue_b=='December':
                sb_end_year.delete(0,'end')
                sb_end_year.insert(0,currentyear)
        elif heresavalue_b==months[1]:
            sb_end_day.delete(0,'end')
            sb_end_day.insert(0,1)
            sb_end_day.config(from_=1,to=14-(days_in_month[1]-currentday))
            if heresavalue_b=='January':
                sb_end_year.delete(0,'end')
                sb_end_year.insert(0,currentyear+1)    
                       
            
def get_spinbox_values():
    months=['January','February','March','April','May','June','July','August','September','October','November','December']
    mm_s=str(months.index(sb_start_month.get())+1).zfill(2)
    dd_s=str(sb_start_day.get()).zfill(2)
    yy_s=str(sb_start_year.get()).zfill(4)
    hh_s=str(sb_start_hour.get()).zfill(2)
    mm_e=str(months.index(sb_end_month.get())+1).zfill(2)
    dd_e=str(sb_end_day.get()).zfill(2)
    yy_e=str(sb_end_year.get()).zfill(4)
    hh_e=str(sb_end_hour.get()).zfill(2)
    entry1="{}-{}-{}-{}".format(mm_s,dd_s,yy_s,hh_s)
    entry2="{}-{}-{}-{}".format(mm_e,dd_e,yy_e,hh_e)
    subprocess.call("sed -i /userstartdate=/c\\userstartdate=funny",shell=True)
    subprocess.call("sed -i /userstartdate=/c\\userstartdate='{}' ../../Run_WRF_GUI".format(entry1),shell=True)
    subprocess.call("sed -i /userenddate=/c\\userenddate='{}' ../../Run_WRF_GUI".format(entry2),shell=True)

############################################################################
############################################################################    

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=gui_color[0])    

        global sb_start_month, sb_start_day, sb_start_year, sb_start_hour
        global sb_end_month, sb_end_day, sb_end_year, sb_end_hour
        lbl = tk.Label(self,text="Choose Simulation Start Time", font=("Arial Bold",40),bg=gui_color[1],foreground="white")
        lbl.grid(row=0,column=0,columnspan=4,sticky=tk.E+tk.W)
        self.columnconfigure(0,weight=1)
        
        lbl_start_month = tk.Label(self,text="Start Month", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_start_month.grid(row=1,column=0,sticky=tk.W,pady=(50,0),padx=(50))
        self.columnconfigure(0,weight=0)
        
        lbl_start_Day = tk.Label(self,text="Start Day", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_start_Day.grid(row=1,column=1,sticky=tk.W,pady=(50,0),padx=(50))
        self.columnconfigure(1,weight=0)
        
        lbl_start_year = tk.Label(self,text="Start Year", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_start_year.grid(row=1,column=2,sticky=tk.W,pady=(50,0),padx=(50))
        self.columnconfigure(2,weight=0)
        
        lbl_start_hour = tk.Label(self,text="Start Hour", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_start_hour.grid(row=1,column=3,sticky=tk.W,pady=(50,0),padx=(50))
        self.columnconfigure(3,weight=1)
        if currentday>=15:
            sb_start_month=tk.Spinbox(self,width=10,font=("Arial Bold",35),value=[months[0]],command=update_spinbox_start)
            sb_start_month.delete(0,'end')
            sb_start_month.insert(0,months[0])
            
        else:
            sb_start_month=tk.Spinbox(self,width=10,font=("Arial Bold",35),value=months,command=update_spinbox_start)
            sb_start_month.delete(0,'end')
            sb_start_month.insert(0,months[-1])
        sb_start_month.grid(column=0,row=2,sticky=tk.W,padx=(50))
        sb_start_month_value=sb_start_month.get()
             
        sb_start_day=tk.Spinbox(self,width=10,font=("Arial Bold",35), from_=user_startdate_range[0], to = user_startdate_range[1])
        sb_start_day.delete(0,'end')
        sb_start_day.insert(0,currentday)
        sb_start_day.grid(column=1,row=2,sticky=tk.W)
        self.columnconfigure(1,weight=0)

        if (currentday <=5) and (currentmonth==1):
            sb_start_year=tk.Spinbox(self,width=10,font=("Arial Bold",35), value=[currentyear-1,currentyear])
        else:
            sb_start_year=tk.Spinbox(self,width=10,font=("Arial Bold",35), value=currentyear)
        sb_start_year.delete(0,'end')
        sb_start_year.insert(0,currentyear)
        sb_start_year.grid(column=2,row=2)
        
        sb_start_hour=tk.Spinbox(self,width=10,font=("Arial Bold",35), from_= 0, to = 18, increment=6)
        sb_start_hour.delete(0,'end')
        sb_start_hour.insert(0,forecasthour)        
        sb_start_hour.grid(column=3,row=2,sticky=tk.W)
        

        lbl_end_month = tk.Label(self,text="End Month", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_end_month.grid(row=3,column=0,sticky=tk.W,pady=(75,0),padx=(50,0))
        self.columnconfigure(0,weight=0)
        
        lbl_end_Day = tk.Label(self,text="End Day", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_end_Day.grid(row=3,column=1,sticky=tk.W,pady=(75,0))
        self.columnconfigure(1,weight=0)
        
        lbl_end_year = tk.Label(self,text="End Year", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_end_year.grid(row=3,column=2,sticky=tk.W,pady=(75,0))
        self.columnconfigure(2,weight=0)
        
        lbl_end_hour = tk.Label(self,text="End Hour", font=("Arial Bold",40),bg=gui_color[0],foreground="white")
        lbl_end_hour.grid(row=3,column=3,sticky=tk.W,pady=(75,0))
        self.columnconfigure(3,weight=1)
        if currentday<=5:
            sb_end_month=tk.Spinbox(self,width=10,font=("Arial Bold",35),value=months[-1],command=update_spinbox_end)
            sb_end_month.delete(0,'end')
            sb_end_month.insert(0,months[-1])
        if currentday>=15:
            sb_end_month=tk.Spinbox(self,width=10,font=("Arial Bold",35),value=months,command=update_spinbox_end)
            sb_end_month.delete(0,'end')
            sb_end_month.insert(0,months[0])
        if (currentday>5) and (currentday<15):
            sb_end_month=tk.Spinbox(self,width=10,font=("Arial Bold",35),value=months,command=update_spinbox_end)
            sb_end_month.delete(0,'end')
            sb_end_month.insert(0,months[-1])
        sb_end_month.grid(column=0,row=4,sticky=tk.W,padx=(50,0))
        sb_end_month_value=sb_end_month.get()

             
        sb_end_day=tk.Spinbox(self,width=10,font=("Arial Bold",35), from_=user_enddate_range[0], to =user_enddate_range[1])
        sb_end_day.delete(0,'end')

        if forecasthour >= 18:
            sb_end_day.insert(0,currentday+1)
        else:
            sb_end_day.insert(0,currentday)
        sb_end_day.grid(column=1,row=4,sticky=tk.W)
        self.columnconfigure(1,weight=0)

        if (currentday >=15) and (currentmonth==12):
            sb_end_year=tk.Spinbox(self,width=10,font=("Arial Bold",35), value=[currentyear,currentyear+1])
        else:
            sb_end_year=tk.Spinbox(self,width=10,font=("Arial Bold",35), value=[currentyear])
        sb_end_year.delete(0,'end')
        sb_end_year.insert(0,currentyear)
        sb_end_year.grid(column=2,row=4)
        
        sb_end_hour=tk.Spinbox(self,width=10,font=("Arial Bold",35), from_= 0, to = 18, increment=6)
        sb_end_hour.delete(0,'end')
        sb_end_hour.insert(0,(forecasthour+6)%24)        
        sb_end_hour.grid(column=3,row=4,sticky=tk.W)

        from Pages.page_two   import PageTwo
        #btn_1 = tk.Button(self,text="Choose Domain",font=("Arial Bold",40),borderwidth=5,bg=gui_color[2],activebackground=gui_color[3],width=20,command=lambda :[reset()])
        btn_1 = tk.Button(self,text="Choose Domain",font=("Arial Bold",40),borderwidth=5,bg=gui_color[2],activebackground=gui_color[3],width=20,command=lambda :[get_spinbox_values(),reset(),controller.show_frame(PageTwo)])
        btn_1.grid(column=1,row=5,columnspan=2,pady=(50,0))

        from Pages.start_page  import StartPage
        btn_2 = tk.Button(self,text="Home",font=("Arial Bold",40),borderwidth=5,bg=gui_color[2],activebackground=gui_color[3],width=20,command=lambda : controller.show_frame(StartPage))
        btn_2.grid(column=1,row=6,columnspan=2,pady=20)


        def reset():    
            if currentday>=15:
                sb_start_month.delete(0,'end')
                sb_start_month.insert(0,months[0])
            
            else:
                sb_start_month.delete(0,'end')
                sb_start_month.insert(0,months[-1])
            sb_start_day.delete(0,'end')
            sb_start_day.insert(0,currentday)
            sb_start_hour.delete(0,'end')
            sb_start_hour.insert(0,forecasthour)
            sb_start_year.delete(0,'end')
            sb_start_year.insert(0,currentyear)

            if currentday<=5:
                sb_end_month.delete(0,'end')
                sb_end_month.insert(0,months[-1])
            if currentday>=15:
                sb_end_month.delete(0,'end')
                sb_end_month.insert(0,months[0])
            if (currentday>5) and (currentday<15):
                sb_end_month.delete(0,'end')
                sb_end_month.insert(0,months[-1])
            if forecasthour >= 18:
                sb_end_day.insert(0,currentday+1)
            else:
                sb_end_day.delete(0,'end')
                sb_end_day.insert(0,currentday)
            sb_end_year.delete(0,'end')
            sb_end_year.insert(0,currentyear)
            sb_end_hour.delete(0,'end')
            sb_end_hour.insert(0,(forecasthour+6)%24)
            
