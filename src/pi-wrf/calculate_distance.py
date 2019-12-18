from math import sin,cos,sqrt,atan2,radians,degrees,pi
#from geopy import distance

def calculate_distances(lon1_input,lon2_input,lat1_input,lat2_input):
    #point_1=(lat1_input,lon1_input)
    #point_2=(lat2_input,lon2_input)
    #user_distance=distance.distance(point_1,point2).km
    #return user_distance
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
    
#mydistance=calculate_distances(-179.67443515,179.33641701,-0.07649884,30.16723003)
#print(mydistance)
