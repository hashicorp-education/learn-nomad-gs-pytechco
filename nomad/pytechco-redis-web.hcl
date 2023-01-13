job "pytechco-redis-web" {
  datacenters = ["dc1"]
  type = "service"

  group "ptc-redis" {
    count = 1
    network {
      port "redis" {
        to = 6379
      }
    }

    service {
      name = "redis-svc"
      port = "redis"
      provider = "nomad"
    }

    task "redis-task" {
      driver = "docker"

      config {
        image = "redis:7.0.7-alpine"
        ports = ["redis"]
      }
    }
  }

  group "ptc-web" {
    count = 1
    network {
      port "web" {
        to = 5000
      }
    }

    service {
      name = "ptc-web-svc"
      port = "web"
      provider = "nomad"
    }

    task "ptc-web-task" {
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
        image = "arussohashi/ptc-web:latest"
        ports = ["web"]
      }
    }
  }
}