from flask import render_template

from app import app

from .auth import *


@app.route("/")
@app.route("/index")
def index():
    user = {
        'logged_in': GoogleAuth.is_logged_in(),
    }
    if user["logged_in"]:
        user['username'] = GoogleAuth.get_user_info()["name"]

    print(requests.get("https://www.googleapis.com/fitness/v1/users/me/dataSources"))

    return render_template('index.html', title='Dashboard', user=user)


@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])


@app.after_request
def add_default_headers(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Authorization"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return resp
