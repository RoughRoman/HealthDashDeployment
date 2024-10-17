#!/bin/bash

# Set the image and container names
IMAGE_NAME="orch_api_code_img"
CONTAINER_NAME="orch_api_code_con"

# Stop and remove the running container if it exists
if [ "$(docker ps -a -q --filter "name=$CONTAINER_NAME")" ]; then
    echo "Stopping and removing container..."
    docker stop "$CONTAINER_NAME"
    docker rm "$CONTAINER_NAME"
else
    echo "No container found with name $CONTAINER_NAME."
fi

# Remove the Docker image if it exists
if [ "$(docker images -q "$IMAGE_NAME")" ]; then
    echo "Removing image..."
    docker rmi "$IMAGE_NAME"
else
    echo "No image found with name $IMAGE_NAME."
fi

echo "Cleanup completed."

# Pause for user input before exiting
read -p "Press any key to continue..."
