from flask import Flask, render_template, redirect, request, session, json
from flask_session.__init__ import Session
from datetime import timedelta, datetime
from Login.login import Check_login
from Trades.main import demo_list_open_order
from Trades.Trade_history import trade_history
import requests

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
#--------------------------------------------------------------------
########################## Home
#--------------------------------------------------------------------
@app.route("/Home", methods=["POST", "GET"])
def App_main_page():
    try:
        if not session.get("Username"):
            return render_template("/Login/index.html")
        else:
            path = session.get('Path')
            now = datetime.now()
            url = f"https://open-api.bingx.com/openApi/swap/v2/quote/klines?symbol=BTC-USDT&interval=5m&startTime=1578492800000&endTime={int(now.timestamp() * 1000)}&limit=1440"
            headers = {'x-api-key': '09ba90f6-dcd0-42c0-8c13-5baa6f2377d0'}

            resp = requests.get(url, headers=headers)
            x = resp.json()
            array_data = []
            array_data_Date = []
            array_data_Open = []
            array_data_High = []
            array_data_Low = []
            array_data_Close = []
            array_data_Volume = []
            print(resp)
            for i in x['data']:
                array_data_Date.append(str(i['time']))
                array_data_Open.append(float(i['open']))
                array_data_High.append(float(i['high']))
                array_data_Low.append(float(i['low']))
                array_data_Close.append(float(i['close']))
                array_data_Volume.append(float(i['volume']))
            list_trades = demo_list_open_order()
            print(list_trades)
            window = 600
            return render_template("/Home/index.html",open=array_data_Open[len(array_data_Open) - window:],
                           close=array_data_Close[len(array_data_Close) - window:],
                           high=array_data_High[len(array_data_High) - window:],
                           low=array_data_Low[len(array_data_Low) - window:],
                           date=array_data_Date[len(array_data_Date) - window:],
                           valoum=array_data_Volume[len(array_data_Volume) - window:], window=600, list_trades=list_trades, user=session.get('Username'), pathmain=path, email=session.get('email'))
    except:
        return render_template("/Error/index.html")


@app.route("/Home/Trade", methods=["POST", "GET"])
def App_Trade():
    try:
        if not session.get("Username"):
            return render_template("/Login/index.html")

        else:
            path = session.get('Path')
            rr = int(request.args.get("rr"))
            obj_trade_history = trade_history(rr)
            list_trade_history = obj_trade_history.start()
            return render_template("/Trade/Trade_history.html",len_list_trade_history=len(list_trade_history), list_trade_history=list_trade_history, user=session.get('Username'), pathmain=path, email=session.get('email'))
    except:
        return render_template("/Error/index.html")

@app.route("/Home/Asset", methods=["POST", "GET"])
def App_Trade():
    try:
        if not session.get("Username"):
            return render_template("/Login/index.html")
        else:
            path = session.get('Path')
            rr = int(request.args.get("rr"))

            obj_trade_history = trade_history(rr)
            list_trade_history = obj_trade_history.start()
            return render_template("/Trade/Trade_history.html",len_list_trade_history=len(list_trade_history), list_trade_history=list_trade_history, user=session.get('Username'), pathmain=path, email=session.get('email'))
    except:
        return render_template("/Error/index.html")
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1001)