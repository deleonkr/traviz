import geopy.distance
import math

def geoDistance(sensor1, sensor2):
    lat1, lon1 = sensorLocationMap[sensor1]
    lat2, lon2 = sensorLocationMap[sensor2]
    distance = geopy.distance.vincenty((lat1, lon1), (lat2, lon2)).miles
    return distance

fname_data="I10_2016_hourly_east-759163-to-763453"
fname_sensorList = "Sensor_list_of_"+fname_data+".csv"
fh_sensorList = open(fname_sensorList)
file_networkDist = open("benchmark_distances.csv")
file_sensorLoc = open("I10_2016_sensor_locationMap.csv")
fo = open("diffDistData.csv","w")

header_flag = 0
ishead=True
sensorLocationMap={}
dataToWrite = []

sensorList=fh_sensorList.read().strip().split(",")

for line in file_sensorLoc:
    if ishead==True:
        ishead=False
    else:
        sensor,lat,lon = line.strip().split(",")
        sensorLocationMap[sensor]=(float(lat),float(lon))

calcDist=[]
for sensorID in range(len(sensorList)-1):
    dist = geoDistance(sensorList[sensorID],sensorList[sensorID+1])
    calcDist.append((sensorList[sensorID],sensorList[sensorID+1],dist))
print(calcDist)
ele = []
for line1 in file_networkDist:
    if header_flag==0:
        header_flag=1
        fo.write("sensor1,sensor2,networkDist,calcDist,diff\n")
    else:
        sensor1,sensor2,netDist = line1.strip().split(",")
        for pair in calcDist:
            if (sensor1 == pair[0]) and (sensor2 == pair[1]):
                newNetworkDist = float(netDist) * (1/1609.344)
                ele = [sensor1,sensor2,str(newNetworkDist),str(pair[2]),str(math.fabs(newNetworkDist - pair[2]))]
                dataToWrite.append(",".join(ele))
if len(dataToWrite)!= 0:
    fo.write("\n".join(dataToWrite)+"\n")
