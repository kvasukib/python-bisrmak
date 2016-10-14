# Kean Freeman
# Script Descriptions
extractInfluxData.py, levelShiftOnInflux.py, levelshift_plotter_influxdb.py, 
collectImagesForCider.py

1. extractInfluxData.py
	This script interacts with the influxDB database to quickly extract 
rtt/timestamp data in preparation for processing with levelshift and so 
on. It is parallelized. After creating .ts files in timeSeriesAndOutputFiles, 
it runs levelShiftOnInflux. This script also generates a stats file, called 
stats.txt, in the same directory. This program uses 15 cores and takes about 
40-50 minutes to complete, usually.

2. levelShiftOnInflux.py
	This script first generates output files from the .ts files in 
timeSeriesAndOutputFiles and then runs levelshift_plotter.py on them, which 
generates images of those files. This program uses 20 cores for the initial 
part. Lastly, it runs collectImagesForCider.py.

3. levelshift_plotter_influxdb.py
	I didn't write this script, I was directed to it by Alex Gamero-Garrido. 
It accepts a .out file (with levelshifts) and plots them along with their 
corresponding .ts points.

4. collectImagesForCider
	This script checks the .out files in /timeSeriesAndOutputFiles/ to see if
they're empty. If not, their corresponding images are moved to Cider along
with a generated XML document that will display them.
