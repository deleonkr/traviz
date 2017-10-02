# This Python script is to combine speed table with distance table and calculate timecost for each sensor pair along the route.

import math
import geopy.distance
import numpy as np


fname_data="I10_2016_hourly_east-759163-to-763453"
fname_sensorList = "Sensor_list_of_"+fname_data+".csv"
fname_speed_calender = "new_Speed_calender_with_route_"+fname_data+".csv"

fh_sensorList = open(fname_sensorList)
fh_speed_calender = open(fname_speed_calender)
fh_sensorLocation = open("I10_2016_sensor_locationMap.csv")

sensorList=fh_sensorList.read().strip().split(",")
speed_table = []

ishead=True
for line in fh_speed_calender:
    if ishead==True:
        ishead=False
    else:
        speed_table.append(map(lambda x:float(x),line.strip().split(",")[2:]))

speed_matrix = np.matrix(speed_table)

ishead=True
sensorLocationMap={}
for line in fh_sensorLocation:
    if ishead==True:
        ishead=False
    else:
        sensor,lat,lon = line.strip().split(",")
        sensorLocationMap[sensor]=(float(lat),float(lon))


def geoDistance(sensor1, sensor2):
    lat1, lon1 = sensorLocationMap[sensor1]
    lat2, lon2 = sensorLocationMap[sensor2]
    distance = geopy.distance.vincenty((lat1, lon1), (lat2, lon2)).miles  # math.sqrt(((float(lat1)-float(lat2))**2 + (float(lon1)-float(lon2))**2))
    return distance

print sensorLocationMap
disList=[]
for sensorID in range(len(sensorList)-1):
    disList.append(geoDistance(sensorList[sensorID],sensorList[sensorID+1]))
print disList

dist_matrix = np.ones((7*24,1)) * np.matrix(disList)
timecost_matrix=3600*dist_matrix / speed_matrix
print timecost_matrix

np.savetxt("Timecost_calender_with_route_"+fname_data+".csv", timecost_matrix, delimiter=",")
