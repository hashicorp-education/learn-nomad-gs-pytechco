job "pytechco-web" {
  type = "service"

  group "ptc-web" {
    count = 1
    network {
      port "web" {
        static = 5000
      }
    }

    service {
      name     = "ptc-web-svc"
      port     = "web"
      provider = "nomad"
    }

    task "ptc-web-task" {
      # Retrieves the .Address and .Port connection values for
      # redis-svc with nomadService and saves them to env vars
      # REFRESH_INTERVAL is how often the UI refreshes in milliseconds
      template {
        data        = <<EOH
{{ range nomadService "redis-svc" }}
REDIS_HOST={{ .Address }}
REDIS_PORT={{ .Port }}
FLASK_HOST=0.0.0.0
REFRESH_INTERVAL=500
{{ end }}
EOH
        destination = "local/env.txt"
        env         = true
      }

      driver = "docker"

      config {
        image = "ghcr.io/hashicorp-education/learn-nomad-getting-started/ptc-web:1.0"
        ports = ["web"]
      }
    }
  }
}