
def update_spinbox_start():
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
