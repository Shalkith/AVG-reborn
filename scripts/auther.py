from hashlib import sha1
from scripts import creds


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
        if x[1] == email and x[7] != 0:
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
