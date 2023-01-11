import redis
import signal
import sys
import time
import random
import os
import argparse

# Employee type values: 
# PRIMARY TASK, SECONDARY TASK, SALARY, WORKING TIME, MIN TASK TIME, MAX TASK TIME, SECONDARY TASK FINDING FACTOR
employee_types = {
    "education_engineer": ["tutorials","customer_happiness",5,12,2,4,4],
    "software_engineer": ["bugs_fixed","customer_happiness",7,15,3,6,6],
    "sales_engineer": ["money","customer_base",4,8,1,3,5],
    "customer_success_engineer": ["customer_happiness","money",3,18,1,5,10]
}

parser = argparse.ArgumentParser(description='Tech Co Simulation Employee')
parser.add_argument('--redis-host', dest='redis_host', action='store', default="localhost", help='The redis hostname (default: localhost)')
parser.add_argument('--redis-port', dest='redis_port', action='store', default=6379, help='The redis port (default: 6379)')
parser.add_argument('--employee-type', dest='employee_type', action='store', choices=employee_types.keys(), help='The type of employee to hire (default: randomizes employee type)')
args = parser.parse_args()

task_time_min = 1
task_time_max = 4
start_time = time.time()
working_time = 10
time_to_complete_tasks = 0
secondary_task_finding_factor = 5
primary_tasks_completed = 0
secondary_tasks_completed = 0

employee_attributes = None
employee_type = None
primary_task = None
secondary_task = None
salary = None

def signal_handler(sig, frame):
    take_employee_offline()

def get_employee_online():
    if args.employee_type:
        employee_attributes = employee_types.get(args.employee_type)
        employee_type = args.employee_type
    else:
        employee_attributes = random.choice(list(employee_types.items()))
        employee_type = employee_attributes[0]
        employee_attributes = employee_attributes[1]
    employee_count = int(r.get("employees").decode())
    global time_to_complete_tasks
    global primary_task
    global secondary_task
    global salary
    primary_task = employee_attributes[0]
    secondary_task = employee_attributes[1]
    salary = employee_attributes[2]
    working_time = employee_attributes[3]
    task_time_min = employee_attributes[4]
    task_time_max = employee_attributes[5]
    secondary_task_finding_factor = employee_attributes[6]
    time_to_complete_tasks = random.randint(task_time_min, task_time_max)

    # Check if there's enough money to pay employee's salary
    if not subtract_money(salary):
        print(f"Sorry, it looks like you don't have the budget for me, a(n) {employee_type}.")
        print("Your company stats: ")
        print("-------------------")
        for key in r.scan_iter("*"):
            print(f"{key.decode(): <25} {r.get(key).decode()}")
        sys.exit(0)
    
    try:
        r.set("employees", employee_count + 1)
    except:
        print("Error registering employee")
    else:
        print(f"I am a(n) {employee_type}, I'm online, and I'm ready to help!")
        print(f"It will take me {time_to_complete_tasks} second(s) to complete my tasks ({primary_task} and {secondary_task}).")
        print(f"I will work for {working_time} second(s) before I have to go offline.")
        print("-----------------------------------------------------------------")
        print(f"There are currently {int(r.get('employees').decode())} employee(s) online including me.")
        print("-----------------------------------------------------------------")

def subtract_money(amount):
    total_money = int(r.get("money").decode())
    if total_money == 0 or total_money - amount < 0:
        return False
    else:
        total_money -= amount
        r.set("money", total_money)
        return True

def do_tasks():
    global primary_task
    global secondary_task
    secondary_task_hit_number = random.randint(1, secondary_task_finding_factor)
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
    global primary_task
    global secondary_task
    employee_count = int(r.get("employees").decode())
    if employee_count > 0:
        try:
            r.set("employees", employee_count - 1)
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

r = redis.Redis(host=args.redis_host, port=args.redis_port)
signal.signal(signal.SIGINT, signal_handler)

get_employee_online()

while True:
    if time.time() - start_time >= working_time:
        take_employee_offline()
        break
    else:
        print("Completing tasks...")
        time.sleep(time_to_complete_tasks)
        do_tasks()