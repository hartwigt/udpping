set autoscale
set grid
set datafile separator ","
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
#set xrange [ "2019-08-02 00:00:00" : "2019-09-09 23:59:59" ]
#set yrange [ -1:200 ] 
set format x "%Y-%m-%d %H:%M:%S"
set xlabel "Zeit"
set ylabel "Lost Packets"
set xtics rotate
set terminal pngcairo size 1920,1080
set output "test.png"
filenames=system('ls -1B *.log')
plot for [file in filenames] file using 1:2 with lines t file
