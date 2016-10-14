from influxdb import InfluxDBClient
import os
import pdb
import bz2
import sys
from multiprocessing import Pool

#Global
# Directories
siblingDir = \
'/project/comcast-ping/TSP/adaptive/siblings/'
asRelationshipFile = \
'/data/external/as-rank-ribs/20160601/20160601.as-rel.txt.bz2'
arkMonitorsFile = \
'/home/amogh/projects/comcast_ping/code/sync/monitor_list_samples.txt'

#Helper Functions

# Returns a list of the ark monitors in monitor_list_samples.txt
def importMonitorList():
	monitorList = []
	with open(arkMonitorsFile) as arkMonitors:
		for monitor in arkMonitors:
			# Removes newline char
			monitorList.append(monitor[:-1])
	return monitorList

def insertSeries(mon, asn, target, destination, link, ind, rtt):
	os.system("curl -i -XPOST 'http://localhost:8086/write?db=example' \
--data-binary 'tsplnk,mon=" + mon + ",asn=" + asn + ",target=" + target + \
",destination=" + destination + ",link=" + link + ",ind=" + ind + " rtt=" + rtt + "'")

# Takes in the resultSet of a query and returns a list of all the values of a 
# tag in the dictionaries of that resultSet
def possibleValuesFromResult(tag, result):
	# The following object contains a list of dictionaries, each dictionary 
	# containing its own series.
	tempList = list(result)
	if len(tempList) > 0:
		seriesList = list(result)[0]
	else:
		return set()
	valuesSet = set()
	for series in seriesList:
		valuesSet.add(series[tag])
	return list(valuesSet)

# Returns a list of neighbor AS's to a particular monitor.
def collectNeighborAS(monitor):
	siblings = set()
	asRelationshipList = []
	with open(siblingDir + monitor + '.sibling.txt') as inFile:
		for line in inFile:
			siblings.add(line[:-1])
	bzFile = bz2.BZ2File(asRelationshipFile)
	asRelationshipList = bzFile.read().splitlines()
	
	neighborASSet = set()
	for line in asRelationshipList:
		if line[0] == '#':
			continue
		tempLine = line.split('|')
		# <AS1>|<AS2>|<Relationship>
		if tempLine[0] in siblings:
			if tempLine[2] == 0:
				neighborASSet.add(tempLine[1])
			continue
		if tempLine[1] in siblings:
			neighborASSet.add(tempLine[0])
	# Was told to hardcode these:
	neighborASSet.add(str(2906))
	neighborASSet.add(str(15169))
	neighborASSet.add(str(20940))
	return list(neighborASSet)

# Returns a list of targets that show up in queries with 'monitor' and 'asn'
def collectUniqueTargets(monitor, asn, client):
	print 'Collecting targets\t' + monitor + '\t' + asn
	queryString = "show series from tsplnk where mon='" + monitor + \
"' and asn='" + asn + "' and ind='1'"
	
	queryResult = client.query(queryString)
	targetsList = possibleValuesFromResult('target', queryResult)
	return targetsList

# Returns a list that holds dictionaries of time/rtt pairs, also known as 
# timeseries data, for the past week.
def collectTimeseriesData(monitor, asn, target, client):
	print 'Collecting timeseries\t' + monitor + '\t' + asn + \
'\t' + target
	queryString = "select rtt from tsplnk where mon='" + monitor + \
"' and asn='" + asn + "' and target='" + target + "' and ind='1' and " + \
" time >= now() - 1w"

	queryResult = client.query(queryString, epoch=0)
	tempList = list(queryResult)
	
	# Prevents error if query returned nothing:
	if len(tempList) > 0:
		return tempList[0]
	return list()

# Takes metadata of container and writes it to a stats file
def writeStatsData(container):
	with open('/home/freeman/influxDB/stats1.txt', 'a') as outFile:
		for monitor in container:
			for AS in container[monitor]:
				outFile.write(monitor + ' ' + AS + ' ' + \
str(len(container[monitor][AS])) + '\n')
	
def exportRTTData(monitor):
	# Container ultimately will hold all timeseries data by the end of 
	# the script. Format is:
	# container[monitor][AS][target][<series index>]['rtt'/'time']
	client = InfluxDBClient('localhost', 8086, 'root', 'root', 'tspmult')
	container = dict()
	
	container[monitor] = dict()
	
	# Collect Neighbor AS's
	neighborASList = collectNeighborAS(monitor)
	for AS in neighborASList:
		container[monitor][AS] = dict()
		
		# Collect Unique Targets
		targetsList = collectUniqueTargets(monitor, AS, client)
		for target in targetsList:
			container[monitor][AS][target] = list()
			
			# Collect Timeseries Data
			container[monitor][AS][target] = \
collectTimeseriesData(monitor, AS, target, client)
			
			# Write data to file, except if there's no data
			if len(container[monitor][AS][target]) <= 0:
				continue
			with open('/home/freeman/influxDB/timeSeriesAndOutputFiles/' \
+ monitor + '_' + AS + '_' + target + '.ts', 'w') as outFile:
				for i in range(0, len(container[monitor][AS][target])):
					# Converting timestamp to seconds and rtt to 
					# milliseconds
					timestamp = \
str(int(container[monitor][AS][target][i]['time']) / 1000000000)
					rtt = \
str(int(container[monitor][AS][target][i]['rtt']))
					outFile.write(timestamp + ' ' + rtt + '\n')
	writeStatsData(container)
	print 'Finished monitor ' + monitor
	
def main():
	# Reset the stats file and ts file directory
	if os.path.isfile('/home/freeman/influxDB/stats1.txt'):
		os.system('rm /home/freeman/influxDB/stats1.txt')
	os.system('rm ./timeSeriesAndOutputFiles/*')
	
	myPool = Pool(15)
	monitorList = importMonitorList()
	
	# Following map takes in the list of monitors
	myPool.map(exportRTTData, monitorList)
	
	# Levelshift, then finished.
	os.system('python /home/freeman/influxDB/levelShiftOnInflux.py')
	print 'All Finished'

main()

