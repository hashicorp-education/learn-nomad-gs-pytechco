# PyTechCo Simulator

A tech company simulator similar to [John Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in that it requires no interaction from the user.

Once set up, employees come online to work on their tasks and log off once complete.

These tasks generate resources for the company that are shown in the company stats section.

New employees will come online only if there is enough `money` to cover their salary.

## Components

There are four components to the simulator: 
- A Redis database holds the resource counts and employee data including their status (online or offline).
- A Flask webapp that shows company resources and information about employees. It automatically refreshes the page.
- A setup script that seeds the database with resources and sets their counts to zero.
- An employee script that brings an employee online, works on tasks, and takes the employee offline when complete. Resources from the tasks are sent to the database.

## Running the simulator

### Python

- Install dependencies.
```
$ pip install -r requirements.txt
$ pip install -r requirements-web.txt
```

- Start a Redis instance (can be a Docker container)
```
$ docker run -it -p 6379:6379 redis:7.0.7-alpine
```

- In another tab, start the webapp.
```
$ python webviewer.py

# Optionally set the Redis host and port as environment variables first.
# They default to localhost and 6379.

$ REDIS_HOST=localhost REDIS_PORT=6379 python webviewer.py
```

- In another tab, run the setup script.
```
$ python setup.py

# Optionally set the budget. The salaries range from 3-7/employee.
# Defaults to 30.
$ PTC_BUDGET=50 python setup.py
```

- Recruit an employee. The type of employee is randomly chosen. You can open multiple tabs to have several employees online at once.
```
$ python employee.py
```

### Nomad

The [`nomad/`](nomad) directory contains job specs to run the simulator on Nomad. Make sure your Nomad environment variables are set: `NOMAD_ADDR` and `NOMAD_TOKEN` if needed.

Change to the directory.
```
$ cd nomad
```

Submit the Redis job.

```
$ nomad job run pytechco-redis.hcl
```

Submit the webapp job. Then open the Nomad UI, navigate to the `pytechco-web` job, click on the allocation, and open the URL listed to see the webapp. 

```
$ nomad job run pytechco-web.hcl
```

Submit the setup job.
```
$ nomad job run pytechco-setup.hcl
```

Dispatch the setup job by providing a value for budget. This is a parameterized batch job so it can be run again and again.
```
$ nomad job dispatch -meta budget="200" pytechco-setup
```

Submit the employee job. This is a cron batch job that will create a new employee every 3 seconds. See [pytechco-employee.hcl](nomad/pytechco-employee.hcl) for the configuration.
```
$ nomad job run pytechco-employee.hcl
```

Shut down the simulator by stopping the jobs in this order.

```
$ nomad job stop -purge pytechco-employee
$ nomad job stop -purge pytechco-web
$ nomad job stop -purge pytechco-redis
$ nomad job stop -purge pytechco-setup
```

### Docker image build command

```
$ docker build -f employee.Dockerfile -t ptc-employee . && \
docker build -f webviewer.Dockerfile -t ptc-web . && \
docker build -f setup.Dockerfile -t ptc-setup . && \
docker image list | grep ptc
```

### Commands to run locally with Docker

```
$ docker run -it -p 6379:6379 redis:7.0.7-alpine
$ docker run -it --network=host ptc-setup
$ python3 webviewer.py 
$ docker run -it --network=host ptc-employee
```