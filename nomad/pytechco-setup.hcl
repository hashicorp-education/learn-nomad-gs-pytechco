job "pytechco-setup" {
  type = "batch"

  parameterized {
    meta_required = ["budget"]
  }

  group "ptc-setup" {
    count = 1

    task "ptc-setup-task" {

      # Retrieves the .Address and .Port connection values for
      # redis-svc with nomadService and saves them to env vars
      # NOMAD_META_budget is read from the job's meta vars
      template {
        data        = <<EOH
{{ range nomadService "redis-svc" }}
REDIS_HOST={{ .Address }}
REDIS_PORT={{ .Port }}
{{ end }}
PTC_BUDGET={{ env "NOMAD_META_budget" }}
EOH
        destination = "local/env.txt"
        env         = true
      }
      driver = "docker"

      config {
        image = "ghcr.io/hashicorp-education/learn-nomad-getting-started/ptc-setup:1.0"
      }
    }
  }
}