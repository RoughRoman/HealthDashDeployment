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
 -e DB_HOST=100.110.194.71 ^
 -e DB_USER=root ^
 -e DB_PASSWORD=laydawg ^
 -e ORGANISATION=italtile ^
 -e TENANT=ItaltileTenant ^
 -e CLIENT_ID=8DEv1AMNXczW3y4U15LL3jYf62jK93n5 ^
 -e REFRESH_TOKEN=zPbeJI9HelA_MXsUnt-48-BvGEjS6lX_AWuXJC8csy-rL ^
 -e TIMESERIES_INTERVAL=120 ^
 -e REALTIME_INTERVAL=60 ^
 -e SCHEMA_NAME=italtile_DB2 ^
 --name %CONTAINER_NAME% %IMAGE_NAME%

echo Docker container %CONTAINER_NAME% started successfully.
pause
