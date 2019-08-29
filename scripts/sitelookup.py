from hashlib import sha1
from scripts import creds


def confirm_site(siteurl):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name

    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from sites where url = '"+siteurl+"'")
    print (query)
    cursor.execute(query)
    validuser  = False
    id,url,name,desc,admin = '','','','',''
    for x in cursor:
        print('vaid site query',x)
        validuser = True
        id,url,name,desc,admin = x[0],x[1],x[2],x[3],x[4]
        return validuser,id,url,name,desc,admin

    return validuser,id,url,name,desc,admin


def site_dir():
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name

    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from sites")
    print (query)
    cursor.execute(query)
    validuser  = False
    id,url,name,desc,admin = '','','','',''
    sitelist = []

    for x in cursor:
        validuser = True
        id,url,name,desc,admin = x[0],x[1],x[2],x[3],x[4]
        sitelist.append([id,url,name,desc,admin])

    return sitelist
