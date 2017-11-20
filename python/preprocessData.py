# This is used to divide our initial dataset by freeway direction, and change the datetime format.

import time
fh = open('traffic_10min_2016_i110.csv')
fo_sensor = open("i110_2016_sensor_locationMap_lb_d.csv","w")
fo2 = open("i110_2016_minute_east_lb_d.csv","w")
fo3 = open("i110_2016_minute_west_lb_d.csv","w")
head_flag = 0
data2 = []
data3 =[]
sensorLocationMap = {}
for line in fh:
    if head_flag==0:
        head_flag=1
        fo2.write("sensor,ts, month,weekdate,hour,minutes,speed,lat,lon\n")
        fo3.write("sensor,ts, month,weekdate,hour,minutes,speed,lat,lon\n")
    else:
        l = line.strip().split(",")
        l_time = l[1]
        st = time.strptime(l_time, '%Y-%m-%d %H:%M:%S')
        weekdate = time.strftime("%w", st)
        hr = time.strftime("%H", st)
        minute = time.strftime("%M", st)
        month = time.strftime("%m", st)
        sensor = l[0]
        speed = l[2]
        lat = l[5]
        lon = l[6]
        direction = l[4]
        if sensor not in sensorLocationMap.keys():
            sensorLocationMap[sensor]=lat+","+lon

        if -118.287439<=float(lon)<=-118.268835 and 33.858136 <= float(lat) <= 34.039149 :
            ele = [sensor, str(time.mktime(st)), month, weekdate, hr, minute, speed, lat, lon]
            if direction=="0":
                data2.append(",".join(ele))
            elif direction=="1":
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
