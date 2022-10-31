provider "azurerm" {
  tenant_id       = var.tenant_id
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  features {}
}
terraform {
  backend "azurerm" {
    resource_group_name  = "Azuredevops"
    storage_account_name = "tfstate3201027946"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
    access_key           = "pyMa4jUZjLdyaIs5Zf2Zr704Tu59ZOebOD4VtH8OzX13779m7B2pHTgzq95b8o87SdoCKFQ3PrBS+AStIcQ1DA=="
  }
}
module "resource_group" {
  source         = "../../modules/resource_group"
  resource_group = var.resource_group
  location       = var.location
}
module "network" {
  source               = "../../modules/network"
  address_space        = var.address_space
  location             = var.location
  virtual_network_name = var.virtual_network_name
  application_type     = var.application_type
  resource_type        = "NET"
  resource_group       = module.resource_group.resource_group_name
  address_prefix_test  = var.address_prefix_test
}

module "nsg-test" {
  source              = "../../modules/networksecuritygroup"
  location            = var.location
  application_type    = var.application_type
  resource_type       = "NSG"
  resource_group      = module.resource_group.resource_group_name
  subnet_id           = module.network.subnet_id_test
  address_prefix_test = var.address_prefix_test
}
module "appservice" {
  source           = "../../modules/appservice"
  location         = var.location
  application_type = var.application_type
  resource_type    = "AppService"
  resource_group   = module.resource_group.resource_group_name
}

module "vm" {
  count = length(var.image_names)
  source              = "../../modules/vm"
  location            = var.location
  resource_type       = "vm"
  resource_group_name = module.resource_group.resource_group_name
  subnet_id           = module.network.subnet_id_test
  name                = var.image_names[count.index]
  image_name          = var.image_names[count.index]
}