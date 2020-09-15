import subprocess
from calculate_distance import calculate_distance
resolution=30      #resolution in km

def set_domain(lons,lats):
    """ Reads user selected lats and lons and configures the
    WPS and WRF Namelists"""
    
    WPS_GEOG_Path='../../WRF_System/lib/WPS_GEOG'
    x_center=(lons[0]+lons[1])/2
    y_center=(lats[0]+lats[1])/2
    gridcells_x=round(round(calculate_distance(min(lons),
                                                max(lons),
                                                min(lats),
                                                min(lats))/(resolution-1)))
                                                #resolition -1 to cover edges of boundary
    gridcells_y=round(round(calculate_distance(min(lons),
                                                min(lons),
                                                min(lats),
                                                max(lats))/(resolution-1)))

    subprocess.call("sed -i /e_we/c\\e_we='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(gridcells_x),shell=True)
    subprocess.call("sed -i /e_we/c\\e_we='{}' "
                    "/pi-wrf/WRF_System/WRFV3/run/namelist.input".format(gridcells_x),shell=True)
    subprocess.call("sed -i /e_sn/c\\e_sn='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(gridcells_y),shell=True)
    subprocess.call("sed -i /e_sn/c\\e_sn='{}' "
                    "/pi-wrf/WRF_System/WRFV3/run/namelist.input".format(gridcells_y),shell=True)
    subprocess.call("sed -i /ref_lat/c\\ref_lat='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(y_center),shell=True)
    subprocess.call("sed -i /ref_lon/c\\ref_lon='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(x_center),shell=True)

    subprocess.call("sed -i /truelat1/c\\truelat1='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(lats[0]),shell=True)
    subprocess.call("sed -i /truelat2/c\\truelat2='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(lats[1]),shell=True)

    subprocess.call("sed -i /pole_lat/c\\pole_lat='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(90-abs(y_center)),shell=True)
    
    subprocess.call("sed -i /stand_lon/c\\stand_lon='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(x_center),shell=True)
    subprocess.call("sed -i /stand_lon/c\\stand_lon='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(x_center),shell=True)
    subprocess.call("sed -i /geog_data_path/c\geog_data_path='{}' "
                    "/pi-wrf/WRF_System/WPS/namelist.wps".format(WPS_GEOG_Path),shell=True)
    
    if (min(abs(lats[0]),abs(lats[1])) < 17) or (max(abs(lats[0]),abs(lats[1])) > 70):
       subprocess.call("sed -i /time_step/c\\time_step=60 "
                       "/pi-wrf/WRF_System/WRFV3/run/namelist.input",shell=True)
    elif max(lats) > 17 and min(lats) < -17:
       subprocess.call("sed -i /time_step/c\\time_step=60 "
                       "/pi-wrf/WRF_System/WRFV3/run/namelist.input",shell=True)
    else:
       subprocess.call("sed -i /time_step/c\\time_step=180 "
                       "/pi-wrf/WRF_System/WRFV3/run/namelist.input",shell=True)
