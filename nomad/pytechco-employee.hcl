job "pytechco-employee" {
  type = "batch"

  periodic {
    cron             = "0/3 * * * * * *"
    prohibit_overlap = false
  }

  group "ptc-employee" {
    count = 1

    task "ptc-employee-task" {

      restart {
        attempts = 2
        delay    = "15s"
        interval = "10s"
        mode     = "fail"
      }

      # Retrieves the .Address and .Port connection values for
      # redis-svc with nomadService and saves them to env vars
      # NOMAD_SHORT_ALLOC_ID is read from the job's runtime vars
      template {
        data        = <<EOH
{{ range nomadService "redis-svc" }}
REDIS_HOST={{ .Address }}
REDIS_PORT={{ .Port }}
PTC_EMPLOYEE_ID={{ env "NOMAD_SHORT_ALLOC_ID"}}
{{ end }}
EOH
        destination = "local/env.txt"
        env         = true
      }
      driver = "docker"

      config {
        image = "ghcr.io/hashicorp-education/learn-nomad-getting-started/ptc-employee:1.0"
        // args = [
        //     "--employee-type", "sales_engineer"
        // ]
      }
    }
  }
}