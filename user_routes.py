@app.route('/<variable>', methods=['GET','POST'])
def site(variable):
    validuser,id,url,name,desc,admin = sitelookup.confirm_site(variable)
    if validuser == True:
        return render_template('usersite.html',sitename=name,sitedesc=desc,siteadmin=admin)
    else:
        return '<link rel="stylesheet" href="/static/css/avg.css">Invalid site. <br>Please <a href="https://twitter.com/avidgamers"><font color="light blue">contact me on Twitter</font></a> if you think this is in error<br><br><a class="button" href="/">Return Home</a>'
