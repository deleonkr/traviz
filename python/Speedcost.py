# This Python script is to calculate average speed between sensor pairs along the route group by weekdate and hour.
import sys
fiName = sys.argv[1] #"I5_2016_minute_west"
fh = open(fiName+".csv")
isHead = True
head =None
data={}
sensorList = []
count = 0
for line in fh:
    count += 1
    if isHead == True:
        head = line.strip().split(",")
        isHead=False
    else:
        sensor, ts, month, weekdate, hour, minute, speed, lat, lon = line.strip().split(",")
        month=str(int(month))
        hour = str(int(hour))
        minute = str(int(minute))
        if (weekdate,hour,minute) not in data.keys():
            tmp={}
            tmp[sensor]=[[ts,speed]]
            data[(weekdate,hour,minute)]= tmp
        else:
            if sensor not in data[(weekdate,hour,minute)].keys():
                data[(weekdate,hour,minute)][sensor]=[[ts,speed]]
            else:
                data[(weekdate,hour,minute)][sensor].append([ts,speed])
        if sensor not in sensorList:
            sensorList.append(sensor)
print(sensorList)

def aveSpeed(wd,hr,mins,sensor1, sensor2):
    list_of_speed_of_sensor1 = data[(wd,hr,mins)][sensor1]
    list_of_speed_of_sensor2 = data[(wd,hr,mins)][sensor2]
    list_of_speed_of_sensor1.sort(key=lambda x:x[0])
    list_of_speed_of_sensor2.sort(key=lambda x:x[0])
    i1=0
    i2=0
    list_of_speed_pairs = []
    while i1<len(list_of_speed_of_sensor1) and i2<len(list_of_speed_of_sensor2):
        if list_of_speed_of_sensor1[i1][0] == list_of_speed_of_sensor2[i2][0]:
            list_of_speed_pairs.append([list_of_speed_of_sensor1[i1][1],list_of_speed_of_sensor2[i2][1]])
            i1+=1
            i2+=1
        elif list_of_speed_of_sensor1[i1][0] > list_of_speed_of_sensor2[i2][0]:
            i2+=1
        else:
            i1+=1
    tmp = list(map(lambda x:(float(x[1])+float(x[0]))/2,list_of_speed_pairs))
    if len(tmp)>0:
        ave_speed = sum(tmp)/len(tmp)
        return ave_speed
    else:
        return -1

speed_route=""
for wd in range(7):
    for hr in range(24):
        for mins in range(0,51,10):
            k = (str(wd), str(hr), str(mins))
            speed_along_the_route = ""
            if k in data.keys():
                for i in range(len(sensorList)-1):
                    if (sensorList[i] in data[k].keys()) and (sensorList[i+1] in data[k].keys()):
                        tmp = aveSpeed(str(wd),str(hr),str(mins),sensorList[i],sensorList[i+1])
                        if tmp != -1:
                            speed_along_the_route+=str(tmp)+","
                            continue
                    speed_along_the_route+="70,"
                speed_along_the_route = speed_along_the_route[:len(speed_along_the_route) - 1] + "\n"
                speed_route += str(wd)+","+str(hr)+","+str(mins)+","+speed_along_the_route
                continue
            else:
                speed_along_the_route="70,"*(len(sensorList)-1)
            speed_along_the_route = speed_along_the_route[:len(speed_along_the_route) - 1] + "\n"
            speed_route += str(wd) + "," + str(hr) + "," + str(mins) + "," + speed_along_the_route

fo_calender_route_Name = "Speed_calender_with_route_"+fiName+"-"+sensorList[0]+"-to-"+sensorList[-1]
fo_calender_route=open(fo_calender_route_Name+".csv","w")
speed_route="weekdate,hour,minute,"+",".join(sensorList[:len(sensorList)-1])+"\n"+speed_route
fo_calender_route.write(speed_route)
fo_calender_route.close()

fo_sensor_list=open("Sensor_list_of_"+fiName+"-"+sensorList[0]+"-to-"+sensorList[-1]+".csv","w")
fo_sensor_list.write(",".join(sensorList))
fo_sensor_list.close()
fh.close()
