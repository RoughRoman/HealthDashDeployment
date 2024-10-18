#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update and upgrade the system packages
echo "Updating and upgrading system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "Installing Docker..."
sudo apt install docker.io -y

# Start and enable Docker service
echo "Starting and enabling Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

# Pull Docker images for Grafana and MySQL
echo "Pulling Docker images..."
sudo docker pull grafana/grafana
sudo docker pull mysql:latest

# Run MySQL container with environment variables
echo "Running MySQL Docker container..."
sudo docker run -d --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=<your-password> \
  -e MYSQL_DATABASE=<database-name> \
  -v /my/own/datadir:/var/lib/mysql \
  -p 3306:3306 mysql:latest

# Run Grafana container
echo "Running Grafana Docker container..."
sudo docker run -d --name grafana-container \
  -p 3000:3000 grafana/grafana

echo "Script completed successfully."

