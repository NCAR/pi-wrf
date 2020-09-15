from math import sin,cos,sqrt,atan2,radians,degrees,pi

def calculate_distance(lon1_input,lon2_input,lat1_input,lat2_input):
    """ calculates the distance between two locations on the globe
    based on their lat/lon coordinates"""
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
