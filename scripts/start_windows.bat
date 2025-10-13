@echo off
REM Windows batch script to start Superset testing environment

echo =================================
echo    Superset OSM Testing Setup
echo =================================

echo.
echo Checking Docker...
docker --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: Docker is not installed or not running
    pause
    exit /b 1
)

echo.
echo Checking Docker Compose...
docker-compose --version
if %ERRORLEVEL% neq 0 (
    echo ERROR: Docker Compose is not installed
    pause
    exit /b 1
)

echo.
echo Building and starting Superset with OSM configuration...
docker-compose up -d

echo.
echo Waiting for services to start (this may take a few minutes)...
timeout /t 30 /nobreak

echo.
echo Checking service status...
docker-compose ps

echo.
echo =================================
echo    Setup Complete!
echo =================================
echo.
echo Superset should be available at: http://localhost:8088
echo Username: admin
echo Password: admin
echo.
echo To test OSM maps:
echo 1. Go to Charts -> Create new chart
echo 2. Choose a dataset with geographic data
echo 3. Select deck.gl visualization types (like deck.gl Scatterplot)
echo 4. Check if OSM tiles are available in the map configuration
echo.
echo To stop the environment, run: docker-compose down
echo.
pause