from datetime import datetime, timedelta
import time

### Add Log Date to the command Line input
def addDate(time_stamp, date_and_time):
  time_str = time_stamp.strftime('%H:%M:%S')
  date_str = date_and_time.strftime('%d/%b/%Y:%H:%M:%S')
  date_time_str = date_str[:11] + ":" + time_str
  added_date_time = datetime.strptime(date_time_str,'%d/%b/%Y:%H:%M:%S')
  return added_date_time

### Convert Date and Time to datetime format string
def convertToDate(string_input, time_zone): 
  converted_date = datetime.strptime(string_input, '%d/%b/%Y:%H:%M:%S')  
  if time_zone != '-0500': 
    converted_date = converted_date + timedelta(hours=1)
  #time_string = converted_date.strftime('%H:%M:%S')
  #logged_time = datetime.strptime(time_string,'%H:%M:%S' )
  return converted_date