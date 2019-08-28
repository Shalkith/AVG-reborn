from flask import Flask, render_template, request,redirect, url_for
import string
import os
from scripts import creds, auther, create_account
from datetime import datetime
import flask_login




import mysql.connector

def dbcheck(query):
    # Connect to server
    cnx = mysql.connector.connect(
        host=creds.mysqlhost,
        port=3306,
        user=creds.mysqlun,
        password=creds.mysqlpw,
        database='avidgamers')

    # Get a cursor
    cur = cnx.cursor()
    # Execute a query
    cur.execute(query)
    result = cur
    data = []
    print(query)
    for x in cur:
        data.append(x)
    try:
        cnx.commit()
    except:
        pass
    return data




app = Flask(__name__)
key = 'jUNrE-I|m,MI9Wr~nG7KK]8I%>zIuf{K*IlV<W<Y-m_Pi?U.w368S4YB+H*3cG8-nG7KK]8I%>zIuf{K*IlV<W<'
app.secret_key = key

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    try:

        user = User()
        print('attempting to confirm',email,'is authed')

        reauthdata = auther.verifyuser(email,'password')
        print('Reauth',reauthdata)
        user.id = reauthdata[1]
        user.uniqueid = reauthdata[0]
        user.role = reauthdata[2]
        user.displayname = reauthdata[3]
        user.uniqueidhash = reauthdata[4]
        user.parentsite = reauthdata[5]

        return user
    except:
        pass

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    password = request.form.get('password')
    if email == None:
        pass
    else:
        authdata = auther.verifyuser(email,password)
    if email == None or authdata[6] !=True:
        return
    user = User()
    user.id = authdata[1]
    user.uniqueid = authdata[0]
    user.role = authdata[2]
    user.displayname = authdata[3]
    user.uniqueidhash = authdata[4]
    user.parentsite = authdata[5]
    user.is_authenticated = authdata[6]

    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
            return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    try:
        authdata = auther.verifyuser(email,password)
        print(authdata)

        if authdata[6] == True:
            user = User()
            user.id = authdata[1]
            user.uniqueid = authdata[0]
            user.role = authdata[2]
            user.displayname = authdata[3]
            user.uniqueidhash = authdata[4]
            user.parentsite = authdata[5]


            flask_login.login_user(user)
            return redirect(url_for('hello'))
    except Exception as e:
        print(e)
        pass
    return render_template('login.html',message="Unauthorized. Bad Username or Password.")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return 'Signup is not ready yet. Please contact me on Twitter for a temp account'
    if request.method == 'GET':
        return render_template('signup.html')
    username = request.form['email']
    sitename = request.form['sitename']
    description = request.form['description']
    url = request.form['url']
    created,message = create_account.create(username,url,description,sitename)
    return render_template('signup.html',message=message)




@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('login.html',message="Logged out.")


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html',message="Unauthorized. Please login first.")



###############


@app.route('/posts/<variable>', methods=['GET','POST'])
def posts(variable):
    if request.method == 'POST':
        postdata = request.values
        postdata = postdata.to_dict()
        now = str(datetime.now()).split('.')[0][:-3]

        validusercheck = auther.confirm_poster(postdata['username'],postdata['unHa'],postdata['unId'])
        print('validusercheck', validusercheck)
        if validusercheck == True:
            dbcheck('insert into posts (parentsite,subject,body,parentthread,postedby,lastupdate,createddate,type) values ("0","'+postdata['postsubject']+'","'+postdata['postbody']+'","'+variable+'","'+postdata['username']+'","'+now+'","'+now+'","post")')


            board = dbcheck('select * from posts where id="'+variable+'"')
            posts = dbcheck('select * from posts where parentsite="0" and (type = "post" and parentthread="'+variable+'") order by lastupdate desc')
            print(posts)
            #do your code here
            return render_template("posts.html",data=posts, board=board)
        else:
            board = dbcheck('select * from posts where id="'+variable+'"')
            posts = dbcheck('select * from posts where parentsite="0" and (type = "post" and parentthread="'+variable+'") order by lastupdate desc')

            return render_template("posts.html",data=posts, board=board, message = 'somthing went wrong. please try again...')

    else:

        board = dbcheck('select * from posts where id="'+variable+'"')
        posts = dbcheck('select * from posts where parentsite="0" and (type = "post" and parentthread="'+variable+'") order by lastupdate desc')
        print(posts)
        #do your code here
        return render_template("posts.html",data=posts, board=board)

@app.route('/thread/<variable>', methods=['GET','POST'])
def thread(variable):
    if request.method == 'POST':
        postdata = request.values
        postdata = postdata.to_dict()
        now = str(datetime.now()).split('.')[0][:-3]
        dbcheck('insert into posts (parentsite,subject,body,parentthread,postedby,lastupdate,createddate,type) values ("0","NULL","'+postdata['postreply']+'","'+variable+'","admin","'+now+'","'+now+'","reply")')
        dbcheck('update posts set lastupdate = "'+now+'" where id ="'+variable+'"')
        threads = dbcheck('select * from posts where id="'+variable+'" or (parentthread="'+variable+'" and type = "reply")')
        board = dbcheck('select * from posts where id="'+variable+'"')
        print(posts)
        #do your code here
        return render_template("thread.html",data=threads, board=board)

    else:

        threads = dbcheck('select * from posts where id="'+variable+'" or (parentthread="'+variable+'" and type = "reply")')
        board = dbcheck('select * from posts where id="'+variable+'"')
        print(posts)
        #do your code here
        return render_template("thread.html",data=threads, board=board)



######### login goes up here ^
app.debug=True

class BenefitTemplateService(object):

    @staticmethod
    def create(params):
        # some validation here

        params['credit_behavior'] = "none"
        return params


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return '404'
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return '500'
    return render_template('404.html'), 404


@app.route('/')
def home():
    var = dbcheck('select * from posts where parentsite="0" and parentthread="0"')
    return render_template('home.html', data = var)

@app.route('/home')
def home2():
    return redirect(url_for('home'))



@app.route('/post')
def newpost():
    return render_template('newpost.html')



@app.route('/general')
def gen():
    return render_template('genboard.html')


@app.route('/about')
def about():
    return render_template('about.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
