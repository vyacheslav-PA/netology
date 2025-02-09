terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "0.129.0"
    }
  }

  required_version = ">=1.8.4"
}
# variable "yandex_cloud_token" {
#   type = string
#   description = "Ввести токен"
# }
provider "yandex" {
  # token  = var.yandex_cloud_token
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  service_account_key_file = file("~/.authorized_key.json")
}