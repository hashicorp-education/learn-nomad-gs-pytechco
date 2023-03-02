import redis
import signal
import sys
import time
import random
import os
import argparse
import json

# Employee type values
employee_types = {
    "education_engineer": {
        "title": "Education Engineer",
        "id": "0",
        "primary_task": "tutorials",
        "secondary_task": "customer_happiness",
        "salary": 5,
        "working_time": 12,
        "min_task_time": 2,
        "max_task_time": 4,
        "secondary_task_finding_factor": 4,
        "status": "offline"
    },
    "software_engineer": {
        "title": "Software Engineer",
        "id": "0",
        "primary_task": "bugs_fixed",
        "secondary_task": "customer_happiness",
        "salary": 7,
        "working_time": 15,
        "min_task_time": 3,
        "max_task_time": 6,
        "secondary_task_finding_factor": 6,
        "status": "offline"
    },
    "sales_engineer": {
        "title": "Sales Engineer",
        "id": "0",
        "primary_task": "money",
        "secondary_task": "customer_base",
        "salary": 4,
        "working_time": 8,
        "min_task_time": 1,
        "max_task_time": 3,
        "secondary_task_finding_factor": 5,
        "status": "offline"
    },
    "customer_success_engineer": {
        "title": "Customer Success Engineer",
        "id": "0",
        "primary_task": "customer_happiness",
        "secondary_task": "money",
        "salary": 3,
        "working_time": 18,
        "min_task_time": 1,
        "max_task_time": 5,
        "secondary_task_finding_factor": 10,
        "status": "offline"
    }
}

parser = argparse.ArgumentParser(description='Tech Co Simulation Employee')
parser.add_argument('--employee-type', dest='employee_type', action='store', choices=employee_types.keys(), help='The type of employee to hire (default: randomizes employee type)')
args = parser.parse_args()

redis_host = os.getenv('REDIS_HOST', default='localhost')
redis_port = os.getenv('REDIS_PORT', default=6379)
employee_id = os.getenv('PTC_EMPLOYEE_ID', default=time.time())

start_time = time.time()
primary_tasks_completed = 0
secondary_tasks_completed = 0

time_to_complete_tasks = 0
employee_attributes = None
employee_type = None
primary_task = None
secondary_task = None
salary = None

def signal_handler(sig, frame):
    take_employee_offline()

def get_employee_online():
    global employee_attributes
    if args.employee_type:
        employee_attributes = employee_types.get(args.employee_type)
        employee_type = args.employee_type
    else:
        employee_attributes = random.choice(list(employee_types.items()))
        employee_type = employee_attributes[0]
        employee_attributes = employee_attributes[1]
    employee_attributes.update({"id": employee_id})
    employee_attributes.update({"status": "online"})
    employee_count = int(r.get("employees").decode())
    global time_to_complete_tasks
    time_to_complete_tasks = random.randint(employee_attributes.get("min_task_time"), employee_attributes.get("max_task_time"))

    # Check if there's enough money to pay employee's salary
    if not subtract_money(employee_attributes.get("salary")):
        print(f"Sorry, it looks like you don't have the budget for me, a(n) {employee_attributes.get('title')}.")
        print("Your company stats: ")
        print("-------------------")
        print(get_stats_from_db())
        sys.exit(0)
    
    try:
        r.set("employees", employee_count + 1)
        set_employee_record_in_db()
    except:
        print("Error registering employee")
    else:
        print(f"I am a(n) {employee_attributes.get('title')}, I'm online, and I'm ready to help!")
        print(f"It will take me {time_to_complete_tasks} second(s) to complete my tasks ({employee_attributes.get('primary_task')} and {employee_attributes.get('secondary_task')}).")
        print(f"I will work for {employee_attributes.get('working_time')} second(s) before I have to go offline.")
        print("-----------------------------------------------------------------")
        print(f"There are currently {int(r.get('employees').decode())} employee(s) online including me.")
        print("-----------------------------------------------------------------")

def get_stats_from_db():
    output = ""
    for key in r.scan_iter("*"):
        if not key.decode().startswith("employee-"):
            output += f"{key.decode(): <25} {r.get(key).decode()}\n"
    return output

def subtract_money(amount):
    total_money = int(r.get("money").decode())
    if total_money == 0 or total_money - amount < 0:
        return False
    else:
        total_money -= amount
        r.set("money", total_money)
        return True

def do_tasks():
    global employee_attributes
    secondary_task_finding_factor = employee_attributes.get("secondary_task_finding_factor")
    secondary_task_hit_number = random.randint(1, secondary_task_finding_factor)
    primary_task = employee_attributes.get("primary_task")
    secondary_task = employee_attributes.get("secondary_task")
    if random.randint(1, secondary_task_finding_factor) == secondary_task_hit_number:
        if r.incr(secondary_task):
            print(f"\tI completed {secondary_task}!")
            global secondary_tasks_completed
            secondary_tasks_completed += 1
        else:
            print("Error completing secondary task")
    if r.incr(primary_task):
        print(f"\tI completed {primary_task}!")
        global primary_tasks_completed
        primary_tasks_completed += 1
    else:
        print("Error completing primary task")

def take_employee_offline():
    global employee_attributes
    primary_task = employee_attributes.get("primary_task")
    secondary_task = employee_attributes.get("secondary_task")
    employee_count = int(r.get("employees").decode())
    if employee_count > 0:
        try:
            r.set("employees", employee_count - 1)
            employee_attributes.update({"status": "offline"})
            set_employee_record_in_db()
        except:
            print("Error taking employee offline")
        else:
            print("I'm going offline, bye!")
    print("-----------------------------------------------------------------")
    print(f"This time I completed:")
    print(f"\t{primary_tasks_completed} primary task(s) ({primary_task})")
    print(f"\t{secondary_tasks_completed} secondary task(s) ({secondary_task})")
    print(f"Company Totals for my tasks:") 
    print(f"\t{r.get(primary_task).decode()} {primary_task}")
    print(f"\t{r.get(secondary_task).decode()} {secondary_task}")
    sys.exit(0)

def set_employee_record_in_db():
    try:
        r.set(f"employee-{employee_attributes.get('id')}-attr", json.dumps(employee_attributes))
    except:
        print("Error updating employee record in the db")

r = redis.Redis(host=redis_host, port=redis_port)
signal.signal(signal.SIGINT, signal_handler)

get_employee_online()

while True:
    if time.time() - start_time >= employee_attributes.get("working_time"):
        take_employee_offline()
        break
    else:
        print("Completing tasks...")
        time.sleep(time_to_complete_tasks)
        do_tasks()