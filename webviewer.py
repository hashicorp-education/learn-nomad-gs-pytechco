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

@app.route("/")
def home():
    return render_template("index.html", stats=stats(), refresh_interval=refresh_interval)

@app.route("/stats")
def stats():
    output = "<table>"
    for key in r.scan_iter("*"):
        if not key.decode().startswith("employee"): # For employees and employee-
            if key.decode() == "money":
                output += f"<tr style='background-color: yellow;'><td>{key.decode()}</td><td>{r.get(key).decode()}</td></tr>"
            else:
                output += f"<tr><td>{key.decode()}</td><td>{r.get(key).decode()}</td></tr>"
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
                output += f"<p><b>{attr.get('title')}</b> <i>{attr.get('id')}</i> is online!<br/>They're working on {attr.get('primary_task')} and {attr.get('secondary_task')} (1/{attr.get('secondary_task_finding_factor')} chance of completion)!<br/>They'll work for {attr.get('working_time')} seconds before going offline.</p>"
    if output == "":
        return {"online_employees": "There are currently no employees online."}
    else:
        return {"online_employees": output}

if __name__ == "__main__":
    app.run(host=flask_host,port=flask_port)