#Reads .speed csv and generates graph stuff from it. This script will be run by the report-speed script automatically. 

import matplotlib as mpl
mpl.use("Agg")
import matplotlib.pyplot as plt
import os
import numpy as np
#Might have to install some of these modules with simple, or yum (google how to get the modules if there is a python error)

#Graphs internet speed from csv file in home directory. Triggered by /bin/report-speed every 3 hours
#You should change this path to path to the one report-speed outputs to
f = open('/home/pi/speed.csv', 'r')
x = []
y1 = []
y2 = []
counter = 0

for i in f:
        h = i.strip()
        p = h.split(",")
        x += p[:1]
        y1 += p[1:2]
        y2 += p[2:3]
        counter += 1

#Converts upload and download string items to floats
red = [float(i) for i in y1]
red2 = [float(i) for i in y2]

plt.grid()
fig, ax = plt.subplots()
plt.plot(y2,y1, 'ro')
plt.xlabel("Upload Speed (Mb/s)")
plt.ylabel("Download Speed (Mb/s")

#Graph "crosshairs"
mean = plt.axhline(np.mean(red), color='r', linestyle='dashed', linewidth=1)
mean1 = plt.axvline(np.mean(red2), color='r', linestyle='dashed', linewidth=1)

#Sets graph "Scope"
plt.xlim((0,3.5))
plt.ylim((25,52))

#Vertical line for the speed we pay for (edit the x= to suite your needs)
p1 = plt.axvline(x=3, ymax=.923, linewidth=1, color='y', ls='solid')

#Horizontal line for the speed we pay for (edit the y= to suite your needs)
plt.axhline(y=50, xmin=0, xmax=0.857, linewidth=1, color='y', ls='solid')

plt.legend([p1, (p1, mean)], ["What We Pay For", "Average"], loc=4)
plt.title("Speeds Every Hour")
plt.savefig('speed.png')

#Opens file "averages" and replaces contents with current calculated upload and download averages.
f = open ('averages.txt', 'w')
f.write( "Average Down: " + str(np.mean(red)) + '\n' + "Average Up: " + str(np.mean(red2)) + '\n' + "Datapoints: " + str(len(y1)))
f.close

#This is a ghetto way to get the graphs to the webserver to display
os.system('sudo mv speed.png /var/www')
#This is a ghetoo way to get the averages to the webserver to display
os.system('sudo mv averages.txt /var/www')
