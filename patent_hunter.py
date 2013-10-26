import sqlite3, csv, sys

"""
Grabs all the patents with given patents
@Param
@option : decides how to interpret the input. (1 = patent number, 2 = inventor last name)
@patinfo : input patent number or inventor
"""
def patent_hunter(option=0, patinfo=""):
    print 'option : ', option
    print 'patent info : ', patinfo
    assert option!=0 and patinfo!="" # option must not be zero
    writer = csv.writer(open('./result.csv','w'))
    psyinfo = '06304546'

    # Citation sqlite3
    if option == 'patnum' or option == '1':
        opensql = sqlite3.connect("/home/minyoon/citation.sqlite3")
    # Inventor sqlite3
    elif option == 'inventor' or option == '2':
        opensql = sqlite3.connect("/home/minyoon/full_disambiguation.sqlite3")

    if opensql!=None:
        cur = opensql.cursor()
        if option == 'patent' or option == '1':
            # list of patent that this patent is referencing
            #cur.execute("SELECT Citation FROM citation WHERE Patent=? LIMIT 50", (patinfo,))
            # list of patent that references this patent
            cur.execute("SELECT Patent FROM citation WHERE Citation=?", (patinfo,))
        elif option == 'inventor' or option == '2':
            cur.execute("SELECT Patent FROM invpat WHERE Lastname = ? Limit 50", (patinfo,))

        for entry in cur.fetchall():
            print entry
    return 1

if __name__ == "__main__":
    patent_hunter(sys.argv[1], sys.argv[2]);
