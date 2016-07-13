#!/bin/sh
#stub script for testing levelshift 
for i in `ls *.ts`:
do
  OUT="${i}.out"
  cat "${i}.ls.txt" |  ~/pythoncode/python-bisrmak/levelshift -B 300 -L 48 > $OUT
  python ~/imc/levelshift_plotter.py "$i $OUT"
done
