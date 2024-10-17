@echo off
rem Set the image and container names
set IMAGE_NAME=orch_api_code_img
set CONTAINER_NAME=orch_api_code_con

rem Stop and remove the running container
docker ps -a -q --filter "name=%CONTAINER_NAME%" >nul
if not errorlevel 1 (
    echo Stopping and removing container...
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
) else (
    echo No container found with name %CONTAINER_NAME%.
)

rem Remove the Docker image
docker images -q %IMAGE_NAME% >nul
if not errorlevel 1 (
    echo Removing image...
    docker rmi %IMAGE_NAME%
) else (
    echo No image found with name %IMAGE_NAME%.
)

echo Cleanup completed.
pause
