# This is used to divide our initial dataset by freeway direction, and change the datetime format.

import time
fh = open("I10_2016.csv")
fo_sensor = open("I10_2016_sensor_locationMap.csv","w")
fo2 = open("I10_2016_hourly_east.csv","w")
fo3 = open("I10_2016_hourly_west.csv","w")
lon_threshold = -118.26
head_flag = 0
data2 = []
data3 =[]
#d={}
sensorLocationMap = {}
for line in fh:
    if head_flag==0:
        head_flag=1
        fo2.write("sensor,ts, month,weekdate,hour,speed,lat,lon\n")
        fo3.write("sensor,ts, month,weekdate,hour,speed,lat,lon\n")
    else:
        l = line.strip().split(",")
        l_time = l[1]
        st = time.strptime(l_time, '%Y%m%d %H:%M')
        weekdate = time.strftime("%w", st)
        hr = time.strftime("%H", st)
        month = time.strftime("%m", st)
        sensor = l[0]
        speed = l[2]
        lat = l[7]
        lon = l[8]
        direction = l[6]
        if sensor not in sensorLocationMap.keys():
            sensorLocationMap[sensor]=lat+","+lon

        if float(lon)<=lon_threshold:
            ele = [sensor, str(time.mktime(st)), month, weekdate, hr, speed, lat, lon]
            if direction=="2":
                # if len(data2)==100:
                #     fo2.write("\n".join(data2)+"\n")
                #     data2 = []
                data2.append(",".join(ele))
            elif direction=="3":
                # if len(data3)==100:
                #     fo3.write("\n".join(data3)+"\n")
                #     data3 = []
                data3.append(",".join(ele))

data2 = sorted(data2,key=lambda x: float(x.split(",")[-1]))
data3 = sorted(data3,key=lambda x: float(x.split(",")[-1]),reverse=True)
if len(data2)!=0:
    fo2.write("\n".join(data2) + "\n")
fo2.close()
if len(data3)!=0:
    fo3.write("\n".join(data3) + "\n")
fo3.close()

s="sensor,lat,lon\n"
for k,v in sensorLocationMap.items():
    s+=k+","+v+"\n"
fo_sensor.write(s)
fo_sensor.close()
