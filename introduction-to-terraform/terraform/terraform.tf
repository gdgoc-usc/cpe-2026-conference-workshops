terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "6.8.0"
    }
  }
  required_version = ">= 1.14"
}

provider "google" {
  project     = "workshop-test-489801"
  region      = "us-central1"
  zone        = "us-central1-a"
}