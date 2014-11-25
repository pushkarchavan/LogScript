import os 
import sys
import re
import date_conv
from datetime import datetime, timedelta
import time

st = time.time()
log_name = sys.argv[1]
file_path = os.getcwd() + '/' + log_name

### Reading from the log file 
with open(file_path) as log:
    logs = log.readlines() 

### Find where the date and time_zone string are 
date_index = date_conv.findDateIndex(logs[1])
page_index = date_conv.findPageIndex(logs[1])

### Get date of the log under consideration
parsed = logs[1].split(" ")
parsed[date_index] = parsed[date_index].replace("[", "")
parsed[date_index+1] = parsed[date_index+1].replace("]", "")
date_insert = date_conv.convertToDate(parsed[date_index], parsed[date_index+1])

### Convert Command Line Dates into DateTime format
start_time = datetime.strptime(sys.argv[2], '%H:%M:%S')
stop_time = datetime.strptime(sys.argv[3], '%H:%M:%S')

### Insert log date into the specified time
stop_time = date_conv.addDate(stop_time, date_insert)
start_time = date_conv.addDate(start_time, date_insert)

### Add a day if stop time is less that start time 
if stop_time < start_time: 
  stop_time = stop_time + timedelta(days=1)


### Capture the Logs in a Specified Time Frame  
def returnSpecifiedTimeLogs(read_log):
  #Make an empty list 
  ret_list = []
  for i in range(len(read_log)):
    logs_parsed = read_log[i].split(" ")
    logs_parsed[date_index] = logs_parsed[date_index].replace("[", "") # Date and Time
    logs_parsed[date_index + 1] = logs_parsed[date_index + 1].replace("]", "") # Time Zone 
    converted_time = date_conv.convertToDate(logs_parsed[date_index], logs_parsed[date_index + 1])
    
    #Break Condition inserted for performance improvement for small time windows
    if converted_time > (stop_time + timedelta(hours=1)):
      break
    if converted_time > start_time and converted_time < stop_time:
      ret_list.append(read_log[i])      
  return ret_list
      
  

### Main Function 
def main():
  # Get logs between Specified Time Frame
  mylogs = returnSpecifiedTimeLogs(logs)
  print "=========================================================================="
  print "There are %s records from %s to %s" %(len(mylogs), start_time,stop_time)  
  
  static_hits = 0
  static_page_hits = 0
  product_hits = 0
  favicon_ico_hits = 0
  shopbjs_hits = 0
  server_hits = 0
  other_hits = 0
  all_hits = 0
  
  
  for i in range(len(mylogs)):    
    logs_parsed = mylogs[i].split(" ")
    url = logs_parsed[page_index]
         
    if re.match('^/static/', url):
      static_hits += 1
    elif re.match('^/staticpage', url):
      static_page_hits += 1
    elif re.match('^/favicon', url):
      favicon_ico_hits += 1
    elif re.match('^/product', url):
      product_hits += 1
    #elif re.match('^/shopbjs', url):
    #  shopbjs_hits += 1
    elif re.match('^/server-status', url):
      server_hits += 1
    else:
      other_hits += 1
      
  
  print "==========================================================================" 
  print "/static/ Hits = %s" %static_hits
  print "/static Hits = %s" %static_page_hits
  print "/product Hits = %s" %product_hits
  print "/favicon.ico Hits = %s" %favicon_ico_hits
  #print "/shopbjs Hits = %s" %shopbjs_hits
  print "/server-status Hits = %s" %server_hits
  print "All Other Hits = %s" %other_hits  
  print "=========================================================================="
  
  processed = (static_hits+static_page_hits+product_hits+favicon_ico_hits+server_hits+other_hits)
  
  print "Page Views = %s" %(other_hits+product_hits+static_page_hits)
  print "=========================================================================="
  
  #print "Processed = %s" %processed
  #print "Leaked Logs  = %s" %(len(mylogs) - processed)
  #print "=========================================================================="
  et = time.time()
  print "Total Time: %s seconds." %(et - st)
  
    
  
if __name__ == "__main__":
   main()
