
files = {'SR-101': open('traffic_10min_2016_sr101.csv', 'w'),
         'I-405': open('traffic_10min_2016_i405.csv', 'w'),
         'I-10': open('traffic_10min_2016_i10.csv', 'w'),
         'I-5': open('traffic_10min_2016_i5.csv', 'w'),
         'I-110': open('traffic_10min_2016_i110.csv', 'w')}

with open('whole data\\traffic_10min_2016.csv') as f:
    for l in f:
        s = l.strip().split(',')
        if s[-2] in files:
            files[s[-2]].write(s[0]+','+s[1]+','+s[2]+','+s[5]+','+s[6]+','+s[3]+','+s[4]+'\n')

for i in files:
    files[i].close()
