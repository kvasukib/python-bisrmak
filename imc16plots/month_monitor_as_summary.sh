#Alex Gamero-Garrido
#looks for interfaces and congested links found for each month
mon="bed-us"
dates="201607"
for i in `cat /project/comcast-ping/plots-agamerog/AS_targets.txt`;
do
 LINKS="$( cat *$i*interfaces* | wc -l)"
 rm ~/sandbox/interfaces.txt
 cat ~/plots/priority_files.txt | grep $i | grep $mon | grep $dates > ~/sandbox/interfaces.txt
 CONG="$(cat ~/sandbox/interfaces.txt | wc -l)" 
 printf "$mon $dates $i $LINKS $CONG \n"
 #printf "$CONG"
done
