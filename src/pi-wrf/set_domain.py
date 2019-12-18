def set_domain(lons,lats):
    WPS_GEOG_Path='../../WRF_System/lib/WPS_GEOG'
    x_center=(lons[0]+lons[1])/2
    y_center=(lats[0]+lats[1])/2
    gridcells_x=round(round(calculate_distances(lons[0],lons[1],lats[0],lats[0]))/30)
    gridcells_y=round(round(calculate_distances(lons[0],lons[0],lats[0],lats[1]))/30)
    subprocess.call("mkdir bacon",shell=True)
    subprocess.call("sed -i /e_we/c\\e_we='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(gridcells_x),shell=True)
    subprocess.call("sed -i /e_we/c\\e_we='{}' ../../WRF_System/lib/dynamic_namelist_input.wrf".format(gridcells_x),shell=True)
    subprocess.call("sed -i /e_sn/c\\e_sn='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(gridcells_y),shell=True)
    subprocess.call("sed -i /e_sn/c\\e_sn='{}' ../../WRF_System/lib/dynamic_namelist_input.wrf".format(gridcells_y),shell=True)
    subprocess.call("sed -i /ref_lat/c\\ ref_lat='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(y_center),shell=True)
    subprocess.call("sed -i /ref_lon/c\\ ref_lon='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(x_center),shell=True)
    subprocess.call("sed -i /stand_lon/c\\ stand_lon='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(x_center),shell=True)
    subprocess.call("sed -i /geog_data_path/c\ geog_data_path = '{}' ../../WRF_System/lib/dynamic_namelist.wps".format(WPS_GEOG_Path),shell=True) 

    #subprocess.call("sed -i /res@tiMainString/c\\res@tiMainString=High Temperatures /home/pi/Desktop/WRF_3.9.1_SMPAR/WRF_System/lib/Plotting_Scripts/Dynamic_High_Temperature",shell=True)
    #subprocess.call("sed -i /res@tiMainString/c\\res@tiMainString=Low Temperatures /home/pi/Desktop/WRF_3.9.1_SMPAR/WRF_System/lib/Plotting_Scripts/Dynamic_Low_Temperature",shell=True)
    #subprocess.call("sed -i /res@tiMainString/c\\res@tiMainString=Rainfall Totals /home/pi/Desktop/WRF_3.9.1_SMPAR/WRF_System/lib/Plotting_Scripts/Dynamic_Precip",shell=True)
    #subprocess.call("sed -i /res@tiMainString/c\\res@tiMainString=Snow Accumulation /home/pi/Desktop/WRF_3.9.1_SMPAR/WRF_System/lib/Plotting_Scripts/Dynamic_Snow",shell=True)

if __name__=='__main':
    set_domain(lons,lats)
