# Configure the Google Cloud provider
provider "google" {
  project = "your-gcp-project-id" # TODO: Replace with your actual GCP Project ID
  region  = "us-central1"
  zone    = "us-central1-a"
}

# Create a firewall rule to allow HTTP traffic
resource "google_compute_firewall" "allow_http" {
  name    = "allow-http-traffic"
  network = "default"

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  # Allow traffic from anywhere
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["web-server"]
}

# Create the virtual machine instance
resource "google_compute_instance" "web_server" {
  name         = "simple-web-server"
  machine_type = "e2-micro" # Cost-effective instance type
  tags         = ["web-server"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-12"
    }
  }

  network_interface {
    network = "default"

    # The access_config block assigns an ephemeral public IP address
    access_config {
      // Leave empty to assign an ephemeral IP
    }
  }

  # Startup script to install Apache and create a simple HTML page
  metadata_startup_script = <<-EOF
    #!/bin/bash
    apt-get update
    apt-get install -y apache2

    # Create the index.html file
    cat <<HTML > /var/www/html/index.html
    <!DOCTYPE html>
    <html>
    <head>
      <title>Terraform GCP Web Server</title>
      <style>
        body { font-family: sans-serif; text-align: center; margin-top: 50px; }
      </style>
    </head>
    <body>
      <h1>Hello from Terraform on GCP!</h1>
      <p>This web server was deployed automatically using a startup script.</p>
    </body>
    </html>
    HTML

    # Ensure Apache is running
    systemctl enable apache2
    systemctl restart apache2
  EOF
}

# Output the public IP address of the web server
output "web_server_ip" {
  description = "The public IP address of the web server"
  value       = google_compute_instance.web_server.network_interface[0].access_config[0].nat_ip
}