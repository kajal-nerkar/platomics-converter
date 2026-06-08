terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "kubernetes" {
  config_path = "~/.kube/config"   # connects to your cluster
}

resource "kubernetes_namespace" "converter" {
  metadata {
    name = "converter"

    labels = {
      app         = "converter"
      environment = "production"
      managed-by  = "terraform"
    }
  }
}