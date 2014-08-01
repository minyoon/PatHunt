import csv, json

with open('patinfo.csv', 'rb') as pc:
    with open('patinfo.json','w') as pj:
        reader = csv.reader(pc)
        flag = True
#        i=0
        patlist = []
        for r in reader:
#            if i > 10:
#                break;
#            else:
#                i = i + 1
            pdict = dict()
            if flag:
                flag = False
                continue
            pdict['Patent'] = r[0]
            pdict['Firstname'] = r[1]
            pdict['Lastname'] = r[2]
            pdict['Street'] = r[3]
            pdict['City'] = r[4]
            pdict['State'] = r[5]
            pdict['Country'] = r[6]
            pdict['Zipcode'] = r[7]
            pdict['GYear'] = r[8]
            pdict['PClass'] = r[9]
            patlist.append(pdict)
            #json.dump(pdict, pj)
        #json.dump(dict({'Patents': patlist}), pj)
        json.dump(patlist, pj)        
