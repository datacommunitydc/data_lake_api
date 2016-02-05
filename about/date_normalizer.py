# Value date normalizer

from datetime import datetime,date,timedelta
import csv
import os
import numpy 

RSVPvsTOTAL = 1

if RSVPvsTOTAL==1:
	spdcFile = open("/Users/DogFish/Downloads/Statistical_Programming_DC_RSVPs.csv", 'U')
	dsdcFile = open("/Users/DogFish/Downloads/Data_Science_DC_RSVPs.csv", 'U')
	didcFile = open("/Users/DogFish/Downloads/Data_Innovation_DC_RSVPs.csv", 'U')
	dvdcFile = open("/Users/DogFish/Downloads/Data_Visualization_DC_RSVPs.csv", 'U')
	dsmdFile = open("/Users/DogFish/Downloads/Data_Science_MD_RSVPs.csv", 'U')
else:
	spdcFile = open("/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/Statistical_Programming_DC_Total_and_Active_Members.csv", 'U')
	dsdcFile = open("/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/Data_Science_DC_Total_and_Active_Members.csv", 'U')
	didcFile = open("/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/Data_Innovation_DC_Total_and_Active_Members.csv", 'U')
	dvdcFile = open("/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/Data_Visualization_DC_Total_and_Active_Members.csv", 'U')
	dsmdFile = open("/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/Data_Science_MD_Total_and_Active_Members.csv", 'U')

spdcRead = csv.reader(spdcFile,delimiter=",")
dsdcRead = csv.reader(dsdcFile,delimiter=",")
didcRead = csv.reader(didcFile,delimiter=",")
dvdcRead = csv.reader(dvdcFile,delimiter=",")
dsmdRead = csv.reader(dsmdFile,delimiter=",")

spdc = [x for x in spdcRead]
dsdc = [x for x in dsdcRead]
didc = [x for x in didcRead]
dvdc = [x for x in dvdcRead]
dsmd = [x for x in dsmdRead]

spdcLen = len(spdc)-1
dsdcLen = len(dsdc)-1
didcLen = len(didc)-1
dvdcLen = len(dvdc)-1
dsmdLen = len(dsmd)-1

if RSVPvsTOTAL==1:
	vx = 0
	dx = 1
else:
	vx = 1
	dx = 0

spdcValues = [0.75*float(x[vx]) for x in spdc[1:spdcLen]]
dsdcValues = [0.75*float(x[vx]) for x in dsdc[1:dsdcLen]]
didcValues = [0.75*float(x[vx]) for x in didc[1:didcLen]]
dvdcValues = [0.75*float(x[vx]) for x in dvdc[1:dvdcLen]]
dsmdValues = [0.75*float(x[vx]) for x in dsmd[1:dsmdLen]]

spdcDates = [x[dx] for x in spdc[1:spdcLen]]
dsdcDates = [x[dx] for x in dsdc[1:dsdcLen]]
didcDates = [x[dx] for x in didc[1:didcLen]]
dvdcDates = [x[dx] for x in dvdc[1:dvdcLen]]
dsmdDates = [x[dx] for x in dsmd[1:dsmdLen]]


spdcDatetimes = [datetime.strptime(d, '%m/%d/%y') for d in spdcDates]
dsdcDatetimes = [datetime.strptime(d, '%m/%d/%y') for d in dsdcDates]
didcDatetimes = [datetime.strptime(d, '%m/%d/%y') for d in didcDates]
dvdcDatetimes = [datetime.strptime(d, '%m/%d/%y') for d in dvdcDates]
dsmdDatetimes = [datetime.strptime(d, '%m/%d/%y') for d in dsmdDates]

allDates = spdcDates + dsdcDates + didcDates + dvdcDates + dsmdDates

allDatetimes = list(set([datetime.strptime(d, '%m/%d/%y') for d in allDates]))
allDatetimes.sort()
allDatesLen = len(allDatetimes)

spdcValueMassage = []
dsdcValueMassage = []
didcValueMassage = []
dvdcValueMassage = []
dsmdValueMassage = []

for k in range(allDatesLen):
	thisDate = allDatetimes[k]
	try:
		xx = spdcDatetimes.index(thisDate)
		spdcValueMassage = spdcValueMassage + [spdcValues[xx]]
	except ValueError:
		spdcValueMassage = spdcValueMassage + [0]

	try:
		xx = dsdcDatetimes.index(thisDate)
		dsdcValueMassage = dsdcValueMassage + [dsdcValues[xx]]
	except ValueError:
		dsdcValueMassage = dsdcValueMassage + [0]

	try:
		xx = didcDatetimes.index(thisDate)
		didcValueMassage = didcValueMassage + [didcValues[xx]]
	except ValueError:
		didcValueMassage = didcValueMassage + [0]

	try:
		xx = dvdcDatetimes.index(thisDate)
		dvdcValueMassage = dvdcValueMassage + [dvdcValues[xx]]
	except ValueError:
		dvdcValueMassage = dvdcValueMassage + [0]

	try:
		xx = dsmdDatetimes.index(thisDate)
		dsmdValueMassage = dsmdValueMassage + [dsmdValues[xx]]
	except ValueError:
		dsmdValueMassage = dsmdValueMassage + [0]

# f  = open('/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/DC2_normed_rsvps.csv','w')
f  = open('/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/DC2_normed_total.csv','w')
f.write('key,value,date\n')
for k in range(allDatesLen):
	f.write(','.join(["DVDC",str(dvdcValueMassage[k]),allDatetimes[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(allDatesLen):
	f.write(','.join(["SPDC",str(spdcValueMassage[k]),allDatetimes[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(allDatesLen):
	f.write(','.join(["DIDC",str(didcValueMassage[k]),allDatetimes[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(allDatesLen):
	f.write(','.join(["DSDC",str(dsdcValueMassage[k]),allDatetimes[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(allDatesLen):
	f.write(','.join(["DSMD",str(dsmdValueMassage[k]),allDatetimes[k].strftime('%m/%d/%y')]))
	f.write("\n")
f.close()


spdcValueMonth = [0]
dsdcValueMonth = [0]
didcValueMonth = [0]
dvdcValueMonth = [0]
dsmdValueMonth = [0]

dc2months = [allDatetimes[0]]

for k in range(allDatesLen):
	thisDate = allDatetimes[k]
	if (thisDate.month==dc2months[-1].month and thisDate.year==dc2months[-1].year):
		spdcValueMonth[-1] = spdcValueMonth[-1] + int(spdcValueMassage[k])
		dsdcValueMonth[-1] = dsdcValueMonth[-1] + int(dsdcValueMassage[k])
		didcValueMonth[-1] = didcValueMonth[-1] + int(didcValueMassage[k])
		dvdcValueMonth[-1] = dvdcValueMonth[-1] + int(dvdcValueMassage[k])
		dsmdValueMonth[-1] = dsmdValueMonth[-1] + int(dsmdValueMassage[k])
	else:
		dc2months = dc2months + [thisDate]
		spdcValueMonth = spdcValueMonth + [0]
		dsdcValueMonth = dsdcValueMonth + [0]
		didcValueMonth = didcValueMonth + [0]
		dvdcValueMonth = dvdcValueMonth + [0]
		dsmdValueMonth = dsmdValueMonth + [0]

dc2monthsLen = len(dc2months)
# f  = open('/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/DC2_month_rsvps.csv','w')
f  = open('/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/DC2_month_total.csv','w')
f.write('key,value,date\n')
for k in range(dc2monthsLen):
	f.write(','.join(["DVDC",str(dvdcValueMonth[k]),dc2months[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(dc2monthsLen):
	f.write(','.join(["SPDC",str(spdcValueMonth[k]),dc2months[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(dc2monthsLen):
	f.write(','.join(["DIDC",str(didcValueMonth[k]),dc2months[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(dc2monthsLen):
	f.write(','.join(["DSDC",str(dsdcValueMonth[k]),dc2months[k].strftime('%m/%d/%y')]))
	f.write("\n")
for k in range(dc2monthsLen):
	f.write(','.join(["DSMD",str(dsmdValueMonth[k]),dc2months[k].strftime('%m/%d/%y')]))
	f.write("\n")
f.close()

#------------------------------------------------------------------------------------------
spdcValueQtr = [0]
dsdcValueQtr = [0]
didcValueQtr = [0]
dvdcValueQtr = [0]
dsmdValueQtr = [0]

dc2Qtrs = [allDatetimes[0]]

# count = 0
# for k in range(allDatesLen):
# 	thisDate = allDatetimes[k]
# 	if (thisDate.month==dc2Qtrs[-1].month and thisDate.year==dc2Qtrs[-1].year):
# 		count++
# 		if (count<4):
# 			spdcValueQtr[-1] = spdcValueQtr[-1] + int(spdcValueMassage[k])
# 			dsdcValueQtr[-1] = dsdcValueQtr[-1] + int(dsdcValueMassage[k])
# 			didcValueQtr[-1] = didcValueQtr[-1] + int(didcValueMassage[k])
# 			dvdcValueQtr[-1] = dvdcValueQtr[-1] + int(dvdcValueMassage[k])
# 			dsmdValueQtr[-1] = dsmdValueQtr[-1] + int(dsmdValueMassage[k])
# 	else:
# 		count = 0
# 		dc2Qtrs = dc2Qtrs + [thisDate]
# 		spdcValueQtr = spdcValueQtr + [0]
# 		dsdcValueQtr = dsdcValueQtr + [0]
# 		didcValueQtr = didcValueQtr + [0]
# 		dvdcValueQtr = dvdcValueQtr + [0]
# 		dsmdValueQtr = dsmdValueQtr + [0]

dc2QtrsLen = len(dc2Qtrs)
f  = open('/Users/dogfish/Documents/Sean/Gonzalez_Associates_LLC/DC2/StreamRSVPs/DC2_qtrs.csv','w')
f.write('key,value,date\n')
count = 0
QTR = 0
write2file = False
for k in range(dc2monthsLen):
	count += 1
	if count<=3:
		QTR += dvdcValueMonth[k]
		date2use = dc2months[k].strftime('%m/%d/%y')
		if count==3:
			QTR = QTR/3
			write2file = True
	if write2file:
		f.write(','.join(["DVDC",str(QTR),date2use]))
		f.write("\n")
		count = 0
		QTR = 0
		write2file = False

count = 0
QTR = 0
write2file = False
for k in range(dc2monthsLen):
	count += 1
	if count<=3:
		QTR += spdcValueMonth[k]
		date2use = dc2months[k].strftime('%m/%d/%y')
		if count==3:
			QTR = QTR/3
			write2file = True
	if write2file:
		f.write(','.join(["SPDC",str(QTR),date2use]))
		f.write("\n")
		count = 0
		QTR = 0
		write2file = False

count = 0
QTR = 0
write2file = False
for k in range(dc2monthsLen):
	count += 1
	if count<=3:
		QTR += didcValueMonth[k]
		date2use = dc2months[k].strftime('%m/%d/%y')
		if count==3:
			QTR = QTR/3
			write2file = True
	if write2file:
		f.write(','.join(["DIDC",str(QTR),date2use]))
		f.write("\n")
		count = 0
		QTR = 0
		write2file = False

count = 0
QTR = 0
write2file = False
for k in range(dc2monthsLen):
	count += 1
	if count<=3:
		QTR += dsdcValueMonth[k]
		date2use = dc2months[k].strftime('%m/%d/%y')
		if count==3:
			QTR = QTR/3
			write2file = True
	if write2file:
		f.write(','.join(["DSDC",str(QTR),date2use]))
		f.write("\n")
		count = 0
		QTR = 0
		write2file = False

count = 0
QTR = 0
write2file = False
for k in range(dc2monthsLen):
	count += 1
	if count<=3:
		QTR += dsmdValueMonth[k]
		date2use = dc2months[k].strftime('%m/%d/%y')
		if count==3:
			QTR = QTR/3
			write2file = True
	if write2file:
		f.write(','.join(["DSMD",str(QTR),date2use]))
		f.write("\n")
		count = 0
		QTR = 0
		write2file = False
f.close()