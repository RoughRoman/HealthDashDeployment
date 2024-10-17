#!/bin/bash

# Set the image and container names
IMAGE_NAME="orch_api_code_img"
CONTAINER_NAME="orch_api_code_con"

# Build the Docker image
echo "Building the Docker image..."
docker build -t "$IMAGE_NAME" .

# Check if a container with the same name is running and stop it
if [ "$(docker ps -a -q --filter "name=$CONTAINER_NAME")" ]; then
    echo "Stopping and removing existing container..."
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
fi

# Run the Docker container
echo "Running the Docker container..."
docker run -d \
  -e DB_HOST="" \
  -e DB_USER="" \
  -e DB_PASSWORD="" \
  -e ORGANISATION="" \
  -e TENANT="" \
  -e CLIENT_ID="" \
  -e REFRESH_TOKEN="" \
  -e TIMESERIES_INTERVAL="" \
  -e REALTIME_INTERVAL="" \
  -e SCHEMA_NAME="" \
  --name "$CONTAINER_NAME" "$IMAGE_NAME"

echo "Docker container $CONTAINER_NAME started successfully."

# Pause for user input
read -p "Press any key to continue..."
