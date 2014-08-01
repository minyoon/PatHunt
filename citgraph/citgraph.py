"""
Python Script to extract data for the patent citation graph
Author : Minyoon Jung (https://github.com/minyoon0205)
"""

import csv
import sqlite3
from collections import Counter


citsq = sqlite3.connect('/data/patentdata/LATEST/citation.sqlite3')
invsq = sqlite3.connect('/data/patentdata/LATEST/invpat.sqlite3')

writer = csv.writer(open('patcitation.csv', 'wb+'))

writer.writerow(['target', 'source']) # csv format

c1 = citsq.cursor()
c2 = invsq.cursor()

# Sampling those patents by IBM
query = "SELECT Patent FROM citation ORDER BY RANDOM() LIMIT 1"
print 'query: ', query
patentQueue=[['06304546']] # list of lists, so that it can represent the depth

maxDegree = 2
degree = 0
print patentQueue

patentSet = set(patentQueue[0])

while len(patentQueue)!=0 and degree < maxDegree:
    print 'depth: ', degree
    patlist = patentQueue.pop(0)
    for pat in patlist:
        c1.execute("SELECT Patent FROM citation WHERE Citation = ?", (pat,))
        rows = c1.fetchall()
        newPatList = []
        for row in rows:
            newPatList.append(row[0])
            patentSet.add(row[0])
            writer.writerow([pat, row[0]])
        patentQueue.append(newPatList)
        print patentQueue
    degree += 1

patinfo = csv.writer(open('patinfo.csv', 'wb+'))
patinfo.writerow(['Patent','Firstname','Lastname','Street','City', 'State', 'Country', 'Zipcode', 'GYear', 'PClass'])
for p in patentSet:
    c2.execute("sELECT Firstname, Lastname, Street, City, State, Country, Zipcode, GYear, Class from invpat where Patent=? and InvSeq=1", (p,))
    r = c2.fetchone()
    if r != None:
        patinfo.writerow([p,r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]])

#close the sqlite sessions
citsq.close()

print "done"
