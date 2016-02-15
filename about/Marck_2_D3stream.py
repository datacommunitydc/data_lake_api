from copy import deepcopy
import csv
import numpy as np
from dateutil import parser

# fh = open("./about/dc2-members-by-group-20160205.csv","U")
with open("./dc2-membership-matrix-20160205.csv","U") as fh:
    read = csv.reader(fh,delimiter=",")
    head = read.next()
    dc2 = [x for x in read]

    begprog = 10; endprog = 18; datecol = 19

    all_dates = np.array([parser.parse(line[k]) for line in dc2 for k in (range(begprog,endprog)+[datecol])])
    unique_dates = np.sort(np.unique(all_dates))
    num_dates = len(unique_dates)

    cast = np.concatenate((unique_dates.reshape(num_dates,1),np.zeros((num_dates,4))),axis=1)

    dc2h = {"DIDC":deepcopy(cast),"DC2":deepcopy(cast),"DEDC":deepcopy(cast),"DSDC":deepcopy(cast),"DVDC":deepcopy(cast), \
            "DWDC":deepcopy(cast),"DCNO":deepcopy(cast),"SPDC":deepcopy(cast),"WDSDC":deepcopy(cast)}
    progs = np.array(["DIDC","DC2","DEDC","DSDC","DVDC","DWDC","DCNO","SPDC","WDSDC"])

    for prog in progs:
        for k in range(0,len(dc2)):
            xp = int(np.where(progs==prog)[0])+begprog
            if dc2[k][xp]!='':
                date = parser.parse(dc2[k][xp])
                xd = int(np.where(dc2h[prog]==date)[0])
                dc2h[prog][xd,1] += 1

    for k in range(0,len(dc2)):
        dates = dc2[k][begprog:endprog]
        this_date = parser.parse(dc2[k][begprog])
        this_prog = progs[0]
        for d in range(1,len(dates)):
            date = dates[d]
            if date!='':
                if parser.parse(date) < this_date:
                    this_date = parser.parse(date)
                    this_prog = progs[d]
        for prog in progs:
            # xp = int(np.where(progs==prog)[0])+begprog
            xd = int(np.where(dc2h[prog]==this_date)[0])
            # if dc2[k][xp]!='':
            #     dc2h[prog][xd,1] += 1
            if prog==this_prog:
                dc2h[prog][xd,3] += 1

    for prog in progs:
        dc2h[prog][0,2] = dc2h[prog][0,1]
        dc2h[prog][0,4] = dc2h[prog][0,3]
        for k in range(1,len(dc2h[prog])):
            dc2h[prog][k,2] = np.sum(dc2h[prog][0:k,1])
            dc2h[prog][k,4] = np.sum(dc2h[prog][0:k,3])

with open('./DC2_Prog_CumulativeMemberships.csv','w') as f:
    f.write('key,value,date\n')
    for prog in progs:
        for row in dc2h[prog]:
            f.write(','.join([prog,str(row[2]),str(row[0])[0:-9]]))
            f.write("\n")

with open('./DC2_DC2_CumulativeMemberships.csv','w') as f:
    f.write('key,value,date\n')
    for prog in progs:
        for row in dc2h[prog]:
            f.write(','.join([prog,str(row[4]),str(row[0])[0:-9]]))
            f.write("\n")

with open('./DC2_Prog_Joined.csv','w') as f:
    f.write('key,value,date\n')
    for prog in progs:
        for row in dc2h[prog]:
            f.write(','.join([prog,str(row[1]),str(row[0])[0:-9]]))
            f.write("\n")

print "Done!"