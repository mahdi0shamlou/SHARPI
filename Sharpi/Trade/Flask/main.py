from flask import Flask, render_template, redirect, request, session, json
from flask_session.__init__ import Session
from datetime import timedelta
from Login.login import Check_login
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=15)
@app.route("/")
def Home():
    try:
        if not session.get("Username"):
            return redirect("/Login")
        path = session.get('Path')
        return redirect(f"/{path}")
    except:
        return render_template("/Error/index.html")
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404/index.html'), 404
@app.errorhandler(504)
def internal_error(error):
    return render_template('504/index.html'), 504
#--------------------------------------------------------------------
########################## Login
#--------------------------------------------------------------------
@app.route("/Login", methods=["POST", "GET"])
def Login():
    try:
        if not session.get("Username"):
            return render_template("/Login/index.html")
        else:
            path = session.get('Path')
            return redirect(f"/{path}")
    except:
        return render_template("/Error/index.html")
@app.route("/Login_check", methods=["POST", "GET"])
def Login_check():
    try:
        if request.args.get("username") is None or request.args.get("pass") is None:
            return redirect("/Login")
        else:
            user = request.args.get("username")
            password = request.args.get("pass")
            Check_login_resualt = Check_login(user, password)
            return Check_login_resualt
    except:
        return render_template("/Error/index.html")
@app.route("/logout")
def logout():
    try:
        session["Username"] = None
        return redirect("/")
    except:
        return render_template("/Error/index.html")
#--------------------------------------------------------------------
########################## End Login
#--------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1001)