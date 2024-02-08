terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host    = "npipe:////.//pipe//docker_engine"
}

resource "docker_image" "redis" {
  name = "bitnami/redis"
}

resource "docker_container" "SaaS_Applications" {
  image = docker_image.redis.image_id
  name = "SaaS_Applications"
  command = ["yes"]
}

resource "docker_image" "traefik" {
  name = "traefik"
}

resource "docker_container" "Edge_Services" {
  image = docker_image.traefik.image_id
  name = "Edge_Services"
  command = ["yes"]
}

resource "docker_image" "kong" {
  name = "kong:latest"
}

resource "docker_container" "API_Management" {
  image = docker_image.kong.image_id
  name = "API_Management"
  command = ["yes"]
}

resource "docker_image" "postgres" {
  name = "postgres:latest"
}

resource "docker_container" "Data_Warehouse" {
  image = docker_image.postgres.image_id
  name = "Data_Warehouse"
  command = ["yes"]
}

resource "docker_image" "spark" {
  name = "apache/spark"
}

resource "docker_container" "Apache_Spark" {
  image = docker_image.spark.image_id
  name = "Apache_Spark"
  command = ["yes"]
}

resource "docker_image" "kube" {
  name = "cloudnativelabs/kube-router"
}

resource "docker_container" "Firewall" {
  image = docker_image.kube.image_id
  name = "Firewall"
  command = ["yes"]
}

