from hashlib import sha1
from scripts import creds


def create_role(sort,rolename,isadmin,isactive,url):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select rolename from siteroles where url = '"+url+"'")
    cursor.execute(query)
    roles = []
    existingrole = False
    import re
    for x in cursor:
        roles.append(x)
    for x in roles:
        print(re.escape(rolename))
        print(re.escape(x[0]))
        if rolename in re.escape(x[0]):
            existingrole = True

    if existingrole == True:
        query = ("update siteroles set rolename='"+rolename+"',is_admin='"+isadmin+"',active='"+isactive+"', sort='"+sort+"' where url = '"+url+"' and rolename = '"+rolename+"'")
        print(query)
    else:
        query = ("insert into siteroles (rolename,is_admin,active,sort,url) values('"+rolename+"','"+isadmin+"','"+isactive+"','"+sort+"','"+url+"')")
        print(query)

    cursor.execute(query)
    cnx.commit()


def edituser(username,role,isactive,url):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("update siteusers set role='"+role+"',active='"+isactive+"'where  user = '"+username+"' and parentsite = '"+url+"'")
    cursor.execute(query)
    cnx.commit()



def lookup_roles(url):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from siteroles where url = '"+url+"' order by sort")
    cursor.execute(query)
    validuser  = False
    roles = []
    for x in cursor:
        roles.append(x)
    return roles



def lookup_users(url):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name
    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from siteusers where parentsite = '"+url+"' order by user")
    cursor.execute(query)
    validuser  = False
    users = []
    for x in cursor:
        users.append(x)
    return users





def confirm_poster(username,hashid,unid):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name

    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select username,id,email from users where username = '"+username+"'")
    print (query)
    cursor.execute(query)
    validuser  = False
    for x in cursor:
        print('vaid user query',x)
        if username == x[0] and (unid == str(x[1]) and hashid == x[2]):
            validuser = True

    return validuser

def verifyuser(email,password):
    email = email.lower()
    import mysql.connector
    #MySQL details. same for all scripts


    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name

    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select * from users where username = '"+email+"'")
    query2 = ("select username,password from users where username='"+email+"'")

    cursor.execute(query)
    validuser  = False

    for x in cursor:
        if x[1].lower() == email and x[7] != 0:
            #print('valid user')
            validuser = True
            id,username,role,displayname,useremail,parentsite,active = x[0],x[1],x[3],x[4],x[5],x[6],x[7]
            #return True
        elif x[1] == email and x[7] == 1:
            print('disabled user')
        else:
            pass


    if validuser != True:
        return '','','','','','',False

    cursor.execute(query2)

    for x in cursor:
        if x[0] == username:
            username,hashedpassword = generate_mysql_hash(username,password)
            if hashedpassword == x[1]:
                #print('password confirmed. authed')
                return id,username,role,displayname,useremail,parentsite,True
            else:
                #print('password failed. not authed')
                return id,username,role,displayname,useremail,parentsite,False


        else:
            #print(x[0]+' is not valid!!!')
            return '','','','','','',False

    return '','','','','','',False


def generate_mysql_hash(username,passw):
    mysql_hash = '*' + sha1(sha1(passw.encode('utf-8')).digest()).hexdigest()

    return username,mysql_hash
