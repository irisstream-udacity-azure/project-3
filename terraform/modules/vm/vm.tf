module "publicip" {
  source           = "../../modules/publicip"
  location         = var.location
  application_type = var.image_name
  resource_type    = "publicip"
  resource_group   = var.resource_group_name
}

resource "azurerm_network_interface" "nic" {
  name                = "${var.name}-${var.resource_type}-nic"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = module.publicip.public_ip_address_id
  }
}

data "azurerm_image" "image" {
  name                = var.image_name
  resource_group_name = "udacity"
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                  = "${var.name}-${var.resource_type}"
  location              = var.location
  resource_group_name   = var.resource_group_name
  size                  = "Standard_B1s"
  admin_username        = "adminuser"
  network_interface_ids = [azurerm_network_interface.nic.id]
  admin_ssh_key {
    username   = "adminuser"
    public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCwIYCv5hFjDeY77EexF8+TBi7TFEOnNztD5ERiQ7k1hSL+MgNDorMCKdt1YrHOOyhoY+q2U+xoBgOGVTbhsDYKlFc+BroQtItkqtETlYYI9DSYo/GGM6QA6TVM/uOM6eZXPXPiUaKmm5zAVSAjLXkfdVY1rweJk9Mow+vrHUuc5fsw6yYh/ue3KkUXI+5UlNRioQ1OcjK3gOked1enBjUu+ZDMtIXCWgYBzdd96MAbxcF1f5ay0Iu6izSkuum0/i0c1S0BSr3WdLciuEpGspZQ54gnyt0sD9O0pf+BdfEo1QznQCbEjwXacntElTiZhcc9C/IsDwUWAtSx9bHDpwD8KeT+PGV3f9PqIHbPt12bXho1Ke19h5PeqW6Nsg6WsXcMt0ZKKCdVRHpkfwPwKk3LoVY7dx+OSbDgaPOhjhqLgAZXn4X2sxMRiuKqExlEaUOGCbaeRk5z7xwdTeXD2DSkkqROz/OBpeXBv7uOZpsGScj3wkKrI88SW8VpfsK0p5U= iris@irisstream-pc"
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_id = data.azurerm_image.image.id
}