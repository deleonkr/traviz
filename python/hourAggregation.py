import sys

minutes_file = sys.argv[1] + '_2016_minute_%s_' + sys.argv[2] + '.csv'
hours_file = sys.argv[1] + '_2016_hourly_%s_' + sys.argv[2] + '.csv'

for direction in ['east', 'west']:
    data = dict()
    with open(minutes_file%(direction,)) as f:
        next(f)
        for line in f:
            columns = line.strip().split(',')
            columns[6] = float(columns[6])
            sensor_time = tuple(list([int(float(columns[1])) // 3600 * 3600]) + [int(x) for x in columns[0:1]])
            if sensor_time not in data:
                data[sensor_time] = list([1, *columns[:5], *columns[6:]])
                continue

            data[sensor_time][0] += 1
            data[sensor_time][6] += columns[6]


    with open(hours_file%(direction,), 'w') as f:
        f.write('sensor,ts,month,weekdate,hour,speed,lat,lon\n')
        for i in sorted(data.keys()):
            data[i][6] = str(data[i][6] / data[i][0])
            f.write(','.join(data[i][1:]) + '\n')
