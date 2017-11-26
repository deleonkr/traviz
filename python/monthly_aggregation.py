import glob
from collections import defaultdict

files = glob.glob('hourly_speed/speed/*')
print(files)
d = defaultdict(int)

for file_ in files:
    month = int(file_.split('\\')[-1].split('.')[0])
    with open(file_) as f:
        for line in f:
            speed = float(line.split(',')[-1].strip())
            if speed < 50:
                d[month] += 1

print(len(d))

with open('monthly_aggregated_congestion.csv', 'w') as f:
    for key in sorted(d.keys()):
        f.write(str(key) + ',' + str(d[key]) +'\n')
