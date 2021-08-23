""" This script is my quick and dirty version of fill the monthly timewatch report.
It only fill a set start and end time, don't expect more, it is good enough for me. 
You can fill your PTOs by hand you lazy basterd :)

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

import requests
import pandas
from datetime import datetime
import time

COMPANY_ID = "" # Company id 
EMP_NAME = "" # Employee name it should be a number must of te time.
EMP_ID = "" # Employee id
PASS_WD = "" # Password 
START_TIME = ("9", "0") # Start time for the day, (HOUR, MINUTES)
END_TIME = ("18", "30") # End time for the day, (HOUR, MINUTES)
FIRST_DAY = 23 # The day the reported month start at your calender
LAST_DAY = 22 # The day the reported month end at your calender

currentMonth = datetime.now().month
currentYear = datetime.now().year

weekmask = "Sun Mon Tue Wed Thu"
custombday = pandas.offsets.CustomBusinessDay(weekmask=weekmask)

days = pandas.bdate_range("{0}-{1}-{2}".format(currentYear, currentMonth -1, FIRST_DAY) ,"{0}-{1}-{2}".format(currentYear, currentMonth, LAST_DAY), freq=custombday)


s = requests.Session()
# Authentication
s.post("https://checkin.timewatch.co.il/punch/punch2.php",data = {"comp": COMPANY_ID, "name": EMP_NAME, "pw": PASS_WD})


#Filling the days with emptiness 
for day in days:
    headers = {"Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                "Referer": r"http://checkin.timewatch.co.il/punch/editwh2.php?ie={0}&e={1}&d={2}&jd={2}&tl={1}".format(COMPANY_ID, EMP_ID, day.strftime("%Y-%m-%d"))}
    data = {"nextdate": "", "task0": "0", "taskdescr0": "", "what0": "1", "e":EMP_ID, "tl":EMP_ID, "c": COMPANY_ID, "d" :day.strftime("%Y-%m-%d"),
            "jd": "2021-{0:02d}-01".format(currentMonth), "allowabsence" : "3", "allowremarks": 1, "emm0" : START_TIME[1], "ehh0": START_TIME[0], "xmm0": END_TIME[1] , "xhh0":END_TIME[0]}
    s.post("https://checkin.timewatch.co.il/punch/editwh3.php", data = data, headers = headers, allow_redirects = True)
    time.sleep(1) # For some reason it won"t work without it...
