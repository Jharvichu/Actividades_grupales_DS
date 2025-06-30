variable "records" {
  description = "Mapa de hostnames a IPs"
  type = map(string)
  validation {
    condition = alltrue([
      for k, v in var.records :
        can(regex("^[a-zA-Z0-9-]+$", k))
    ])
    error_message = "Hostname debe ser sin espacios."
  }
}

output "dns_map" {
  value = var.records
}

# terraform init
# terraform plan -var-file="test.tfvars"