# PyTechCo Simulator

## BUILD

```
docker build -f employee.Dockerfile -t ptc-employee . && \
docker build -f webviewer.Dockerfile -t ptc-web . && \
docker build -f setup.Dockerfile -t ptc-setup . && \
docker image list | grep ptc
```

## DEPLOY

```
docker run -it -p 6379:6379 redis:7.0.7-alpine
docker run -it --network=host ptc-setup
python3 webviewer.py 
docker run -it --network=host ptc-employee
```

## Build Images

### Employee

This image contains the code for running an employee container. An employee will complete tasks and send results to a running Redis container. See [employee.py](employee.py).

```
$ docker build -f employee.Dockerfile -t ptc-employee .
```

### Viewer

This image contains the code for viewing the results stored in the Redis container via a webapp. See [viewer.py](viewer.py).

```
$ docker build -f webviewer.Dockerfile -t ptc-web .
```

## Run Containers

- Start Redis
```
$ docker run -it -p 6379:6379 redis:7.0.7-alpine
```

- Run `setup.py` to seed Redis. Hostname and port can be passed with the `--redis-host` and `--redis-port` flags. A budget for the tech company can be specified with `--budget`.

```
$ python3 setup.py [--redis-host="host.domain.com" --redis-port=6380 --budget=100]
```

- Start the viewer container. Hostname and port can be passed with the `--redis-host` and `--redis-port` flags.
```
$ docker run -it --network=host ptc-viewer
```

- Start as many employee containers as you like. Hostname and port can be passed with the `--redis-host` and `--redis-port` flags. The type of employee can be passed with the `--employee-type` flag. Check the help menu for the list of available types.
```
$ python employee.py -h
usage: employee.py [-h] [--redis-host REDIS_HOST] [--redis-port REDIS_PORT]
                   [--employee-type {education_engineer,software_engineer,sales_engineer,customer_success_engineer}]

Tech Co Simulation Employee

optional arguments:
  -h, --help            show this help message and exit
  --redis-host REDIS_HOST
                        The redis hostname (default: localhost)
  --redis-port REDIS_PORT
                        The redis port (default: 6379)
  --employee-type {education_engineer,software_engineer,sales_engineer,customer_success_engineer}
                        The type of employee to hire (default: randomizes
                        employee type)
```

```
$ docker run -it --network=host ptc-employee
```


# TODO
- add persistent storage for redis container
```
$ docker run --name some-redis -d redis redis-server --save 60 1 --loglevel warning
```