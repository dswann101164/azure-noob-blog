---
title: "Terraforming Azure Networks"
date: 2025-09-08
summary: "Step-by-step guide to setting up VNets and subnets in Azure with Terraform."
tags: [terraform, azure, networking]
---

# Terraforming Azure Networks

In this guide, we’ll create a hub-spoke network in Azure with Terraform.

```hcl
resource "azurerm_virtual_network" "hub" {
  name                = "hub-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = "eastus"
  resource_group_name = "rg-network"
}
