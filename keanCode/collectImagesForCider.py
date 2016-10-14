# Kean Freeman
# This script checks the .out files in /timeSeriesAndOutputFiles/ to see if 
# they're empty. If not, their corresponding images are moved to Cider along 
# with a generated XML document that will display them.

# imports
import os
import pdb

# main
print 'Selecting important .out files...'
# CHANGE THIS BLOCK TO CHANGE CRITERIA FOR .out FILES THAT WILL BE DISPLAYED
# Now select all the .out files that aren't empty:
itemsInDir = os.listdir('./timeSeriesAndOutputFiles/')
importantOutFiles = []
for item in itemsInDir:
	# If it ends in 'out'
	if item.split('.')[-1] == 'out':
		if os.path.getsize('./timeSeriesAndOutputFiles/' + item) > 0:
			importantOutFiles.append(item)
importantOutFiles.sort()

# Now import the xml document and, after the line containing:
# '        <xhtmlcode>'
# insert the next line for every image to import:
# '        <img src="./[NAME OF IMAGE]"></img>'
imageTagString = '        <img src="./images/[NAME OF IMAGE]"></img>'
xmlFile = []
with open('./imageHolderFormat.xml') as inFile:
	xmlFile = inFile.readlines()
	
# Find line with '<xhtmlcode>'
lineNumber = 0
for i in range(0, len(xmlFile)):
	if '<xhtmlcode>' in xmlFile[i]:
		lineNumber = i
		break

# Insert image tags after that line
for i in range(0, len(importantOutFiles)):
	# Add name of file and levelshift data below image
	levelshiftData = ''
	with open('./timeSeriesAndOutputFiles/' + importantOutFiles[i]) as inFile:
		levelshiftData = inFile.read()
	levelshiftData = levelshiftData.replace('\n', '<br />')
	addedLine = imageTagString.replace('[NAME OF IMAGE]', \
importantOutFiles[i] + '.png') + '<br /><p>' + importantOutFiles[i] + \
'</p><p>' + levelshiftData + '</p><br />'
	xmlFile.insert(lineNumber + i + 1, addedLine)

# Move images and xml file to cider at:
# /home/freeman/private_xml/influxDB
print 'Moving to Cider...'
with open('/tmp/influxGraphs.xml', 'w') as outFile:
	for line in xmlFile:
		outFile.write(line + '\n')

os.system('scp /tmp/influxGraphs.xml \
keanfree@cider.caida.org:/home/freeman/private_xml/influxDB/')
os.system('rm /tmp/influxGraphs.xml')

for item in importantOutFiles:
	os.system('scp ./timeSeriesAndOutputFiles/' + item + '.png' + \
' keanfree@cider.caida.org:/home/freeman/private_xml/influxDB/images/')


