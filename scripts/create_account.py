from hashlib import sha1
from scripts import creds


def create(username,url,desc,sitename):
    import mysql.connector
    u = creds.mysqlun # MySQL username
    p = creds.mysqlpw # MySQL password
    h = creds.mysqlhost # MySQL server
    db = 'avidgamers' # MySQL datanase name

    cnx = mysql.connector.connect(user=u, password=p,host=h,database=db)
    cursor = cnx.cursor(buffered=True)
    query = ("select username,id from users where username = '"+username.lower()+"'")
    query2 = ("select url,id from sites where url = '"+url.lower()+"'")
    print (query)
    print (query)
    message = ''
    count = cursor.execute(query)
    userexists = False
    print('len count',count)

    for x in cursor:
        print('results:',x)
        print(username.lower(),x[0].lower())
        if username.lower() == x[0].lower():
            userexists = True
            message = message+ 'Username already taken. '
            print(message)

    cursor.execute(query2)
    for x in cursor:
        if url.lower() == x[0].lower():
            userexists = True
            message = message+ 'URL already taken. '


    print('lower username:',username.lower())
    if username.isalnum() == True:
        print('username formatted correctly')
        pass
    else:
        userexists = True
        message = message+ 'Username must contain only numbers and letters. '
    if url.isalnum() == True:
        print('url formatted correctly')
        pass
    else:
        userexists = True
        message = message+ 'URL must contain only numbers and letters. '

    print('print: ',userexists,message)
    if userexists == True:
        print('should exit now with message:',message)
        return False,message
    else:
        print('generating password')
        print()
        print()
        print()
        print()
        passw = genpass(8)
        print('Password:',passw)
        username,passhash = generate_mysql_hash(username,passw)
        createuser = 'insert into users values(0,"'+username+'","'+passhash+'","Site Admin","'+username+'","'+genpass(42)+'","'+url+'",True)'
        print(createuser)
        cursor.execute(createuser)
        cnx.commit()
        query = ("select id,username from users where username = '"+username+"'")
        cursor.execute(query)
        for x in cursor:
            print(x[0])
            userid = x[0]
        createsite = 'insert into sites values(0,"'+url+'","'+sitename+'","'+desc+'","'+str(userid)+'")'
        createboard = 'insert into posts values(0,"'+url+'","'+sitename+'","'+desc+'","0","NULL","NULL","NULL","board")'

        cursor.execute(createsite)
        cursor.execute(createboard)
        cnx.commit()
        message = 'Site Created! Your password is: '+passw
        print(message)
        return True,message

def genpass(leng):
    # generate a password with length "passlen" with no duplicate characters in the password
    import random
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    passlen = leng
    p =  "".join(random.sample(s,passlen ))
    return p


def generate_mysql_hash(username,password):
    mysql_hash = '*' + sha1(sha1(password.encode('utf-8')).digest()).hexdigest()

    return username,mysql_hash
