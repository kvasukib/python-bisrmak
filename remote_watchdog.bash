#check if program running
if ! program="$(ps -aux | grep sc_remoted | grep allowother)"; then
	logfile=/project/comcast-ping/bdrmap-bismark/sc_remoted.log.txt
	#echo "not running"
	date
	echo "No program found. Restarting sc_remoted"
	cd /home/agamerog/sockets; rm OW*
	cd ~/scamper/bin
	./sc_remoted -4 -P 31337 -U /project/comcast-ping/sockets-bismark/ -O allowother -O tka -O allowgroup >> $logfile 2>&1 &
else
	date
	echo "running"
fi 
