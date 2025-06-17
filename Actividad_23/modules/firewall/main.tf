variable "rules" {
  description = "Lista de reglas de firewall"
  type = list(object({
    port = number
    cidr = string
  }))

  validation {
    condition = alltrue([
      for rule in var.rules :
        rule.port > 0 && rule.port < 65536
    ])
    error_message = "Puerto inválido, debe estar desde: 1-65535"
  }
}

output "policy" {
  value = jsonencode({ rules = var.rules })
}

# terraform init
# terraform plan -var-file="test.tfvars"