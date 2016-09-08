#crawler to print IP address of links with evidence of congestion
#ls *far*out > ~/far_list.txt
for i in `cat ~/plots/post_levelshift/bed-us_google.txt`;
do
MONTH="$(echo $i | awk -F"." '{print $3}')"
MONITOR="$(echo $i | awk -F"." '{print $1}')"
TARGET="$(echo $i | awk -F"." '{print $2}')"
ID="$(echo $i | awk -F"." '{print $4}')"
EXT="$(echo $i | awk -F"." '{print $5}')"
cd /project/comcast-ping/plots-agamerog/$MONITOR/$MONTH/
printf "$MONITOR.$TARGET.$MONTH.$ID.$EXT\n"
head $MONITOR.$TARGET.$MONTH.$ID.$EXT
printf "\n"
#echo $PATH
#NEAR="$(ls *near*out | grep $ID)"
#python /home/agamerog/pythoncode/python-bisrmak/imc16plots/filter_levelshift.py $i $NEAR 
done
