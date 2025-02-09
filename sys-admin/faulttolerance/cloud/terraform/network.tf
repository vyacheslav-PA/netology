resource "yandex_vpc_network" "network-1" {
  name = "network-1"
}

resource "yandex_vpc_subnet" "subnet-1" {
  zone        = "ru-central1-a"
  name           = "subnet-1"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["172.17.10.0/24"]
}

resource "yandex_lb_target_group" "target-group-1" { # создать таргет группу
  name      = "target-group-1"

  target {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    address   = yandex_compute_instance.vm[0].network_interface.0.ip_address
  }

  target {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    address   = yandex_compute_instance.vm[1].network_interface.0.ip_address
  }
}


resource "yandex_lb_network_load_balancer" "balancer-1" { # создать балансировщик нагрузки
  name = "balancer-1"

  listener {
    name = "my-listener"
    port = 80
    external_address_spec {
      ip_version = "ipv4"
    }
  }

  attached_target_group {
    target_group_id = yandex_lb_target_group.target-group-1.id

    healthcheck {
      name = "http"
      http_options {
        port = 80
        path = "/"
      }
    }
  }
}
