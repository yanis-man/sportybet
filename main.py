from flask import Flask, Response, redirect, render_template, request, session

from controllers.ApiController import ApiController
from controllers.HomeController import HomeController
from controllers.AuthController import AuthController

ApiController = ApiController()
HomeController = HomeController()
AuthController = AuthController()

app = Flask(__name__, template_folder="./templates")

app.config['SESSION_PERMANENT'] = False
app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
@app.route("/")
def home():
    fetched_fixtures = HomeController.index()
    return render_template("home/index.html", fixtures=fetched_fixtures)


@app.route("/home/getBet", methods=["GET"])
def getBet():
    return "hello"

@app.route("/api/populate", methods=["GET"])
def populate():
    ApiController.populateTodayFixture()
    return 'ok'

@app.route("/api/placeBet", methods=["POST"])
def placeBet():
    if not session['connected']:
        return redirect('/')
    ApiController.placeBet(request.get_json(), session['user_id'])
    return 'ok'

@app.route("/auth/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        register_result = AuthController.register(request.form)
        if register_result != -1:
            _connect_user(register_result)
            return redirect('/')
    return render_template("/auth/register.html")

@app.route("/auth/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        login_result = AuthController.login(request.form)
        if login_result != -1:
            _connect_user(login_result)
            return redirect('/')

    return render_template("/auth/login.html")
    
def _connect_user(user_id):
    session['user_id'] = user_id
    session['connected'] = True
if __name__ == "__main__":
    app.run(debug=True)