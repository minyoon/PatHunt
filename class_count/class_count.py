import csv
import sqlite3
from collections import Counter

#sqlpath = '~/Minyoon/uspto_inventor_disambiguated_201307016.sqlite3'
sqlpath = '../../../Minyoon/uspto_inventor_disambiguated_201307016.sqlite3'
invsq = sqlite3.connect(sqlpath)
csvfile = open('count_classes.csv', 'wb+')
writer = csv.writer(csvfile)


cur = invsq.cursor()
#companies = ['%Apple%Inc%']
#companies = ['%int%bus%mac%']
companies = ['%']

query = "SELECT Class, COUNT(*), AppYear FROM invpat WHERE Assignee LIKE ? GROUP BY Class"
print 'query: ', query

for company in companies:
    # class_counter : counts classes by year
    class_counter = dict()
    cur.execute(query, (company,))
    rows = cur.fetchall()
    for row in rows:
        if row[0]!=None:
            # Start counting each classes by specific years
            for cls in row[0].split('/'):
                round_factor = 2.0
                year = int(round(int(row[2]) / round_factor) * round_factor)
                if year not in class_counter:
                    class_counter[year] = Counter()
                class_counter[year][cls] += row[1]
    ## Now Extract the Most Assigned Patent Classes
    ## and Find out which classes are commonly seen
    classes_seen = []
    for k in class_counter.keys():
        most_class = class_counter[k].most_common(1)
        classes_seen += [mc[0] for mc in most_class]
    classes_seen = list(set(classes_seen))
    writer.writerow(['date'] + classes_seen) # csv format
    for year in sorted(class_counter.keys()): # ordered year
        writer.writerow([year] + [class_counter[year][cls] for cls in classes_seen])

#close the csv and sqlite sessions
csvfile.close()
invsq.close()

print "done"
