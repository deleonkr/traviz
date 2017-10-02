# traviz
journalism + engineering traffic project


## Description for timecost csv file:

eg. Timecost_calender_with_route_I10_2016_hourly_east-759163-to-763453.csv

HEADER:
- **weekdate**: 0 -> monday, 1 -> tuesday, ..., 6 -> sunday
- **hour**: From 0 to 23
- **759163	763646 ...	718419**: They are sensors on the route from santa monica to downtown. The order is the real order from west to east. Values under this column is the timecost between current sensor (column name) and next sensor(next column name) for specific weekdate and hour. The unit is "Second".
- **total/sec	total/min**:  Sum of current row, which means the total timecost for this route for specific weekdate and hour.
