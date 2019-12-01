from flask import render_template

from dateutil.parser import parse as parse_date
from datetime import datetime

from app import app

from .auth import *
from app.provider import *

labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]


@app.route("/")
@app.route("/index")
def index():
    user = {
        'logged_in': GoogleAuth.is_logged_in(),
    }
    if user["logged_in"]:
        user['username'] = GoogleAuth.get_user_info()["name"]

    month_completed_tasks = {}
    try:
        print("Google Tasks")
        tasks = GoogleTasksProvider.get_data()
        for task_list_key in tasks.keys():
            list_tasks = tasks[task_list_key]
            for task in list_tasks:
                if "completed" in task:
                    completed_date = parse_date(task["completed"])
                    if completed_date.year != datetime.now().year:
                        continue

                    if completed_date.month not in month_completed_tasks:
                        month_completed_tasks[completed_date.month] = 1
                    else:
                        month_completed_tasks[completed_date.month] += 1
        for i in range(1, 12+1):
            if i not in month_completed_tasks:
                month_completed_tasks[i] = 0
    except Exception as e:
        print(e)

    try:
        print("Google Fit")
        data = GoogleFitProvider.get_data()
        f = open("test.txt", "w")
        f.write(str(data))
        f.flush()
        f.close()
    except Exception as e:
        print(e)
    return render_template('index.html', title='Dashboard', user=user, max=round(max(*month_completed_tasks.values())), labels=labels,
                           values1=month_completed_tasks.values(), label1="Completed Tasks",
                           values2={1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, label2="Fitness")


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
