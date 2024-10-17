@echo off
rem Set the image and container names
set IMAGE_NAME=orch_api_code_img
set CONTAINER_NAME=orch_api_code_con

rem Build the Docker image
docker build -t %IMAGE_NAME% .

rem Check if a container with the same name is running and stop it
docker ps -a -q --filter "name=%CONTAINER_NAME%" >nul
if not errorlevel 1 (
    echo Stopping existing container...
    docker stop %CONTAINER_NAME%
    docker rm %CONTAINER_NAME%
)

rem Run the Docker container
docker run -d ^
 -e DB_HOST= ^
 -e DB_USER= ^
 -e DB_PASSWORD= ^
 -e ORGANISATION= ^
 -e TENANT= ^
 -e CLIENT_ID= ^
 -e REFRESH_TOKEN= ^
 -e TIMESERIES_INTERVAL= ^
 -e REALTIME_INTERVAL= ^
 -e SCHEMA_NAME= ^
 --name %CONTAINER_NAME% %IMAGE_NAME%

echo Docker container %CONTAINER_NAME% started successfully.
pause
