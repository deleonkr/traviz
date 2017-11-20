# This Python script is to combine speed table with distance table and calculate timecost for each sensor pair along the route.

import math
import geopy.distance
import numpy as np
import glob

files = glob.glob('hourly data\\Sensor*hourly*-*-to-*.csv')
for fil in files:
    parts = fil.split('\\')[1].split('.')[0].split('_')
    fname_data = '_'.join(parts[3:])
    print(fname_data)
    pre = parts[3]
    suf = ''
    if pre == 'I110':
        suf = '_' + parts[7] + '_' + parts[8][0]

    fname_sensorList = "hourly data\\Sensor_list_of_"+fname_data+".csv"
    fname_speed_calender = "hourly data\\Speed_calender_with_route_"+fname_data+".csv"

    fh_sensorList = open(fname_sensorList)
    fh_speed_calender = open(fname_speed_calender)
    fh_sensorLocation = open(pre + "_2016_sensor_locationMap" + suf + ".csv")
    fh_sensorDistance = open("benchmark_distances.csv")

    sensorList=fh_sensorList.read().strip().split(",")
    print(sensorList, len(sensorList))
    speed_table = []
    i = 0;
    ishead=True
    for line in fh_speed_calender:
        if ishead==True:
            ishead=False
            i = i + 1;
        else:
            try:
                i = i + 1;
                speed_table.append(list(map(lambda x:float(x),line.strip().split(",")[2:])))
            except ValueError:
                print("error on line ",i)

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

    disList=[]
    sensorPair=[]
    for sensorID in range(len(sensorList)-1):
        sensorPair.append((sensorList[sensorID],sensorList[sensorID+1]))

    ishd = True
    dist = dict()
    for fLine in fh_sensorDistance:
        if ishd == True:
            ishd = False
        else:
            sensor1,sensor2,netDist = fLine.strip().split(",")
            for pair in sensorPair:
                if (sensor1 == pair[0]) and (sensor2 == pair[1]):
                    newNetworkDist = float(netDist) * (1/1609.344)
                    dist[pair[0], pair[1]] = newNetworkDist

    for pair in sensorPair:
        if pair not in dist:
            dist[pair] = geoDistance(*pair)

        disList.append(dist[pair])

    print(disList, len(disList))
    print(speed_matrix.shape)
    dist_matrix = np.ones((7*24,1)) * np.matrix(disList)
    print(dist_matrix.shape)
    timecost_matrix=3600*dist_matrix / speed_matrix

    np.savetxt("hourly data\\Timecost_calender_with_route_"+fname_data+".csv", timecost_matrix, delimiter=",")
