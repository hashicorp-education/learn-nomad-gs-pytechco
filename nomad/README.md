- Run the redis-web job to set up the database
```
$ nomad job run pytechco-redis.hcl
```

- Run the web job to set up the frontend viewer
```
$ nomad job run pytechco-web.hcl
```

- Run and dispatch the setup job with a value for `budget` to seed the database with values
```
$ nomad job run pytechco-setup.hcl
$ nomad job dispatch -meta budget="200" pytechco-setup
```

- Run the employee batch job to start employees working
```
$ nomad job run pytechco-employee.hcl
```

- Optional: Run the garbage collector to remove dead batch jobs from the UI
```
$ nomad system gc
```