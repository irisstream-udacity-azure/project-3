resource "azurerm_network_interface" "nic" {
  name                = "${var.name}-${var.resource_type}-nic"
  location            = var.location
  resource_group_name = var.resource_group_name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = "${var.subnet_id}"
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${var.public_ip_id}"
  }
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                  = "${var.name}-${var.resource_type}"
  location              = var.location
  resource_group_name   = var.resource_group_name
  size                  = "Standard_DS2_v2"
  admin_username        = "adminuser"
  network_interface_ids = [azurerm_network_interface.nic.id]
  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }
  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }
  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}