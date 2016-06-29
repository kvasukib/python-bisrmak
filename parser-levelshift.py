#input: time-series file from create_ts.pl
#output: levelshift.cc-readable file 
# coding: utf-8

# In[2]:

import csv
import sys

#Input and output files
input_file = str(sys.argv[1])
output_file = input_file + '.ls.txt'
    
with open(input_file, 'rb') as f: #import file

    reader = csv.reader(f, delimiter=' ') #read file into variable reader, delimited using space
    g = open(output_file,'w+')
    for row in reader: #for as long as there is file
            
        #read values from file: IP, TTL, ICMP checksum
        timestamp = row[0]
        rtt = str((int(row[4]))/10) #dividing by 10 to obtain ms
            
    	#format data for levelshift.cc to read:
    	# timestamp value
    	line = timestamp + ' ' + rtt + '\n'
    	g.write(line) # python will convert \n to os.linesep
            
f.close() #close files
g.close()
    

