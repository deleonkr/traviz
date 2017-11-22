import numpy as np

data_file = 'whole data\\traffic_10min_2016.csv'
avg_file = 'traffic_2016_bottom15.csv'

data = dict()
with open(data_file) as f:
    next(f)
    for line in f:
        columns = line.strip().split(',')
        columns[2] = float(columns[2])
        sensor = int(columns[0])
        if sensor not in data:
            data[sensor] = list([1, *columns[:1], *columns[2:6]])
            continue

        data[sensor][0] += 1
        data[sensor][2] += columns[2]

for i in data:
    data[i][2] /= data[i][0]
print([[x[1][2], x[0]] for x in data.items()][:15])
values = np.array(list(data.values()))
l = values[np.array([x[2] for x in values]).argpartition(15)[:15]]

with open(avg_file, 'w') as f:
    f.write('sensor,speed,lat,lon,freeway\n')
    for i in l:
        f.write(','.join(i[1:]) + '\n')
