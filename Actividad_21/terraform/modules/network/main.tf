variable "cidr_block" {}

output "network_cidr" {
  value = var.cidr_block
}