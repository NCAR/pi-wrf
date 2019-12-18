from calculate_distance import *
from math import sin,cos,sqrt,atan2,radians
from subprocess import Popen, PIPE
import subprocess

def calculate_distances(lon1_input,lon2_input,lat1_input,lat2_input):
    #calculates distance between to points on globe and returns value in Km
    R=6373
    lat1=radians(lat1_input)
    lon1=radians(lon1_input)
    lat2=radians(lat2_input)
    lon2=radians(lon2_input)
            
    distance_lon=abs(lon2-lon1)
    distance_lat=abs(lat2-lat1)

    a=sin(distance_lat/2)**2+cos(lat1)*cos(lat2)*sin(distance_lon/2)**2
    c=2*atan2(sqrt(a),sqrt(1-a))
    distance=R*c

    if distance_lon <= pi:
        return distance
    else:
        distance_short=distance
        distance_lon=pi
        a=sin(distance_lat/2)**2+cos(lat1)*cos(lat2)*sin(distance_lon/2)**2
        c=2*atan2(sqrt(a),sqrt(1-a))
        distance_long=2*R*c-distance_short
        return distance_long

resolution=30      #resolution in km

def set_domain(lons,lats):
    WPS_GEOG_Path='../../WRF_System/lib/WPS_GEOG'
    x_center=(lons[0]+lons[1])/2
    y_center=(lats[0]+lats[1])/2
    gridcells_x=round(round(calculate_distances(min(lons),max(lons),min(lats),min(lats))/(resolution-1))) #resolition -1 to cover edges of boundary
    gridcells_y=round(round(calculate_distances(min(lons),min(lons),min(lats),max(lats)))/(resolution-1))

    subprocess.call("sed -i /e_we/c\\e_we='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(gridcells_x),shell=True)
    subprocess.call("sed -i /e_we/c\\e_we='{}' ../../WRF_System/lib/dynamic_namelist_input.wrf".format(gridcells_x),shell=True)
    subprocess.call("sed -i /e_sn/c\\e_sn='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(gridcells_y),shell=True)
    subprocess.call("sed -i /e_sn/c\\e_sn='{}' ../../WRF_System/lib/dynamic_namelist_input.wrf".format(gridcells_y),shell=True)
    subprocess.call("sed -i /ref_lat/c\\ref_lat='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(y_center),shell=True)
    subprocess.call("sed -i /ref_lon/c\\ref_lon='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(x_center),shell=True)

    subprocess.call("sed -i /truelat1/c\\truelat1='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(lats[0]),shell=True)
    subprocess.call("sed -i /truelat2/c\\truelat2='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(lats[1]),shell=True)

    subprocess.call("sed -i /pole_lat/c\\pole_lat='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(90-abs(y_center)),shell=True)
    
    subprocess.call("sed -i /stand_lon/c\\stand_lon='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(x_center),shell=True)
    subprocess.call("sed -i /stand_lon/c\\stand_lon='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(x_center),shell=True)
    subprocess.call("sed -i /geog_data_path/c\geog_data_path='{}' ../../WRF_System/lib/dynamic_namelist.wps".format(WPS_GEOG_Path),shell=True) 
    
    if (min(abs(lats[0]),abs(lats[1])) < 17) or (max(abs(lats[0]),abs(lats[1])) > 70):
       subprocess.call("sed -i /time_step/c\\time_step=60 ../../WRF_System/lib/dynamic_namelist_input.wrf",shell=True)
    elif max(lats) > 17 and min(lats) < -17:
       subprocess.call("sed -i /time_step/c\\time_step=60 ../../WRF_System/lib/dynamic_namelist_input.wrf",shell=True)
    else:
       subprocess.call("sed -i /time_step/c\\time_step=180 ../../WRF_System/lib/dynamic_namelist_input.wrf",shell=True)
