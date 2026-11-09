@echo off
docker build -t crud-app . && docker run -d -p 8000:8000 --name crud-container crud-app
pause
