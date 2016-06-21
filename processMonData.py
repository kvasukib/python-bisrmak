import os
import subprocess
import pdb

# Globals

# Dictionary used for remembering ASNs for AS's
ASNs = { 'netflix':2906, 'google':15169, 'akamai':20940, 'cogent':174, \
'level3':3356, 'tata':6453 }
# List used for remembering list of Bismark monitors
bMonitors = [ 'OWC43DC7A3EDEC', 'OWE8DE27B72366', 'OW744401937CAA', \
'OWA021B7A9BE39', 'OWA021B7A9BF95', 'OWC43DC79D8EBC', 'OWC43DC7A3EE22',
'OWC43DC7A3F0D4', 'OWE8DE27B708D2', 'OWE8DE27B72513', 'OW04A151A3102E',
'OWC43DC7A3EE34', 'OW74440171A157', 'OW2CB05D873788', 'OWC43DC7B0AE78',
'OW04A151A310A9']

# Helper Functions
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Main
def main():
	fileName = \
'/home/amogh/projects/comcast_ping/code/sync/monitor_list_samples.txt'
    
	# Collecting .wart information from all Ark monitors
	with open(fileName) as monitorList:
		bordermapDirName = ''
		for monitor in monitorList:
			# Removes newline and adds to bMonitors
			bMonitors.append(monitor[:-1])

		# Also collecting warts from bMonitors as well
		for monitor in bMonitors:
			# Confirm that month folders aren't already present
			# Need to figure out which months data is available for, then
			bordermapDirName = \
'/project/comcast-ping/TSP/adaptive/mon_data/<monitor_name>/bdrmap-state/warts/current/'
			bordermapDirName = bordermapDirName.replace('<monitor_name>', monitor, 1)
            
			# lsOutput holds all the names of the wart files.
			lsOutput = (subprocess.check_output('ls ' + bordermapDirName, \
shell=True)).split('\n')
			# Filtering out non- .wart.gz files
			for i in lsOutput:
				if '.warts.gz' not in i:
					lsOutput.remove(i)
			
			if len(lsOutput) < 1:
				# contains no wart data
				continue
			# Make the monitor's folder if it doesn't exist
			folderName = '/project/comcast-ping/plots-agamerog/' + monitor
			if (not os.path.isdir(folderName)):
				os.system('mkdir ' + folderName)
			
			# Make a list of all the dates of the wart files using the 
			# 'date' program. Removing last character due to newline output
			wartFileDates = []
			for wartFile in lsOutput:
				wartFileDates.append((subprocess.check_output(\
'date +%Y%m -r ' + bordermapDirName + wartFile, shell=True))[:-1])
			
			# Process the earliest/biggest wart file for each month, if that
			# month file doesn't already exist.
			# 
			# 1. Figure out all the unique months for the current monitor.
			uniqueWartFileDates = []
			for date in wartFileDates:
				if date not in uniqueWartFileDates:
					uniqueWartFileDates.append(date)
			# 2. For each unique month, find out if it needs processing. 
			# Making the assumption that if the folder doesn't exist at 
			# this time, then it hasn't been processed. 
			
			# Collect the date folder names, if there are any
			try:
				dateFilenames = (subprocess.check_output('ls -d ' + \
folderName + '/*/ 2>/dev/null', shell=True)).split('\n')
				print monitor + '\'s wart files have been processed before'
				continue
			except subprocess.CalledProcessError:
				print 'Wart file has not been processed before'
				dateFilenames = []
				
			# Make sure they are actully date folders
			for i in dateFilenames:
				if not isInt(i[-2]):
					dateFilenames.remove(i)
			
			# 3. Collect the sizes of all the files for processing.
			fileSizes = []
			for wart in lsOutput:
				# Removes newline character as well
				fileSizes.append((subprocess.check_output(\
'stat --format="%s" ' + bordermapDirName + wart, shell=True))[:-1])
			
			# 4. Process a month if it hasn't been done yet. Processing 
			# involves finding the earliest/largest wart file in that month.
			#
			# Create a threshold of size to determine the minimum size 
			# required to be a valid wart file. My threshold is 2/3 the size 
			# of the average wart file in a month to be valid.
			print '\nProcessing ' + monitor + '\'s wart files'
			for date in uniqueWartFileDates:
				if date in dateFilenames:
					continue
				dateFolderLocation = folderName + '/' + date + '/'
				os.system('mkdir ' + dateFolderLocation)
				# Collect wart files with this 'date'
				wartFileIndices = []
				for i in range(0, len(wartFileDates)):
					if date == wartFileDates[i]:
						wartFileIndices.append(i)
				# The threshold of size == avgWartSize * (2/3)
				avgWartSize = 0
				for i in wartFileIndices:
					avgWartSize = avgWartSize + int(fileSizes[i])
				avgWartSize = avgWartSize / len(wartFileIndices)
				threshold = int((avgWartSize * 2) / 3)
				# Loop through the warts until one of decent size is picked.
				# Otherwise defaults to the first one.
				processedWart = lsOutput[wartFileIndices[0]]
				for i in wartFileIndices:
					if int(fileSizes[i]) >= threshold:
						processedWart = lsOutput[i]
						break
				# 5. Process the picked wart by moving it to its month file,
				# decompressing it, and running sc_bdrmap on it.
				os.system('cp ' + bordermapDirName + processedWart + ' ' + \
dateFolderLocation + processedWart)
				os.system('gzip -d ' + dateFolderLocation + processedWart)
				# sc_bdrMap execution
				instruction = '/home/agamerog/bdrmap/sc_bdrmap -a /project/\
comcast-ping/plots-agamerog/current.prefix2as -r \
/project/comcast-ping/plots-agamerog/current.as-rel -x /project/comcast-ping/\
plots-agamerog/current.peering -v /project/comcast-ping/plots-agamerog/\
siblings/' + monitor + '.sibling.txt -d 4 ' + dateFolderLocation + processedWart[:-3] + \
' > ' + dateFolderLocation + monitor + '.' + date + '.router-blocks'
				os.system(instruction)
				# compress wart file afterwards
				print 'Compressing wart file'
				os.system('gzip ' + dateFolderLocation + processedWart[:-3])
				print 'Moved wart file and used sc_bdrmap on wart file for ' +\
'time ' + date
				###
				###TODO:
				### If you want to brute-force the plotter scripts, use dateFolderLocation
				# os.system('parallel ' + commandString1 + commandString2 ....)
			print "end"
    
main()
