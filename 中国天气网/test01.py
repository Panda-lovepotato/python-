#!/usr/bin/python3
import datetime

x = datetime.date(2022, 3, 1)
x -= datetime.timedelta(days=1)
print(x.strftime("%Y%m%d"))