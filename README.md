# traviz
journalism + engineering traffic project


## Description for timecost csv file:

eg. Timecost_calender_with_route_I10_2016_hourly_east-759163-to-763453.csv

* header
- weekdate
0 -> monday
1 -> tuesday
...
6 -> sunday
- hour
From 0 to 23
- 759163	763646 ...	718419
This are sensors on the route from santa monica to downtown. The order is the real order from west to east.
The value is the timecost between this sensor (column name) and next sensor(next column name). The unit is second.
- total/sec	total/min
Sum of this row, which means the total timecost for this route on specific weekdate and hour.
