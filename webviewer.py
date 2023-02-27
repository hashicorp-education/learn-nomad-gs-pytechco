import redis
import time
import sys
import os
import json
from flask import Flask, render_template

redis_host = os.getenv('REDIS_HOST', default='localhost')
redis_port = os.getenv('REDIS_PORT', default=6379)
flask_host = os.getenv('FLASK_HOST', default='localhost')
flask_port = os.getenv('FLASK_PORT', default=5000)
refresh_interval = os.getenv('REFRESH_INTERVAL', default=1000)

r = redis.Redis(host=redis_host, port=redis_port)

app = Flask(__name__, template_folder=".")

def translate_task_for_stats(task_name):
    task_name_proper = ""
    if task_name == "money":
        task_name_proper = "Money"
    elif task_name == "customer_base":
        task_name_proper = "New Customers"
    elif task_name == "customer_happiness":
        task_name_proper = "Customer Happiness"
    elif task_name == "tutorials":
        task_name_proper = "Tutorials Written"
    elif task_name == "bugs_fixed":
        task_name_proper = "Bugs Fixed"
    return task_name_proper

def translate_task(task_name):
    task_name_proper = ""
    if task_name == "money":
        task_name_proper = "Generating revenue"
    elif task_name == "customer_base":
        task_name_proper = "Growing the customer base"
    elif task_name == "customer_happiness":
        task_name_proper = "Increasing customer happiness"
    elif task_name == "tutorials":
        task_name_proper = "Writing technical tutorials"
    elif task_name == "bugs_fixed":
        task_name_proper = "Fixing bugs"
    return task_name_proper

def get_task_icon(task_name):
    icon = ""
    if task_name == "money":
        icon = "&#x1F4B5"
    elif task_name == "customer_base":
        icon = "&#x1F46D"
    elif task_name == "customer_happiness":
        icon = "&#x1F601"
    elif task_name == "tutorials":
        icon = "&#x1F4Da"
    elif task_name == "bugs_fixed":
        icon = "&#x1F41B"
    return icon

@app.route("/")
def home():
    return render_template("index.html", stats=stats(), refresh_interval=refresh_interval)

@app.route("/stats")
def stats():
    output = "<table class='table table-hover'>"
    for key in r.scan_iter("*"):
        if not key.decode().startswith("employee"): # For employees and employee
            if key.decode() == "money":
                output += f"""
                <tr class='row row-cols-auto table-warning'>
                <td class='col-6'>{get_task_icon(key.decode())} {translate_task_for_stats(key.decode())}</td>
                <td class='col'>{r.get(key).decode()}</td>
                </tr>
                """
            else:
                output += f"""
                <tr class='row row-cols-auto'>
                <td class='col-6'>{get_task_icon(key.decode())} {translate_task_for_stats(key.decode())}</td>
                <td class='col'>{r.get(key).decode()}</td>
                </tr>
                """
    output += "</table>"
    if output == "<table></table>":
        return {"stats": "DB hasn't been seeded yet."}
    else:
        return {"stats": output}

@app.route("/employees_online")
def get_employees_online_from_db():
    output = ""
    for key in r.scan_iter("*"):
        if key.decode().startswith("employee-"):
            attr = json.loads(r.get(key).decode())
            status = attr.get("status")
            if status == "online":
                output += f"""
                <div class="alert-info">
                <dl class="row row-cols-auto">
                <dt class="col-6">&#x1F469 Employee ID</dt>
                <dd class="col-6">{attr.get('id')}</dd>
                <dt class="col-6">&#x1F3F7 Employee Title</dt>
                <dd class="col-6">{attr.get('title')}</dd>
                <dt class="col-6">&#x1F4DD Primary Task</dt>
                <dd class="col-6">{get_task_icon(attr.get('primary_task'))} {translate_task(attr.get('primary_task'))}</dd>
                <dt class="col-6">&#x1F5D2 Secondary Task</dt>
                <dd class="col-6">{get_task_icon(attr.get('secondary_task'))} {translate_task(attr.get('secondary_task'))}</dd>
                <dt class="col-6">&#x1F340 Chance of Completing Secondary Task</dt>
                <dd class="col-6">(1/{attr.get('secondary_task_finding_factor')})</dd>
                <dt class="col-6">&#x1F558 Shift Length (seconds)</dt>
                <dd class="col-6">{attr.get('working_time')}</dd>
                </dl>
                </div>
                """
    if output == "":
        return {"online_employees": "There are currently no employees online."}
    else:
        return {"online_employees": output}

if __name__ == "__main__":
    app.run(host=flask_host,port=flask_port)