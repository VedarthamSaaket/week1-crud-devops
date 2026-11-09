# Week 1–13 DevOps CRUD Project (without Kubernetes)

## Files
- `main.py`: FastAPI CRUD API, request logging, Prometheus metrics.
- `requirements.txt`: Python dependencies.
- `test_main.py`: pytest CRUD test.
- `Dockerfile`: builds the FastAPI image.
- `deploy.bat`: builds and starts the API container (fresh setup).
- `prometheus.yml`: Prometheus scrape configuration.
- `grafana-run.bat`: starts standalone Grafana.
- `main.tf`: Terraform local-file example.
- `.github/workflows/ci.yml`: GitHub Actions CI workflow.

## Run locally
```powershell
python -m pip install -r requirements.txt
python -m pytest -v
uvicorn main:app --reload
```
API docs: http://127.0.0.1:8000/docs
Metrics: http://127.0.0.1:8000/metrics

## Docker
Run once on a fresh setup:
```powershell
docker build -t crud-app .
docker run -d -p 8000:8000 --name crud-container crud-app
```
Or use `.\deploy.bat` instead of those two commands. Do not run both initial deployment methods.

## Prometheus
Keep FastAPI running on port 8000. In another PowerShell window, from this folder:
```powershell
docker run -d --name prometheus -p 9090:9090 -v "${PWD}/prometheus.yml:/etc/prometheus/prometheus.yml" prom/prometheus
```
Prometheus UI: http://localhost:9090
Targets: http://localhost:9090/targets

Prometheus scrapes FastAPI at `host.docker.internal:8000`.

## Grafana
Start Grafana:
```powershell
.\grafana-run.bat
```
Grafana UI: http://localhost:3000
Default first-login credentials: `admin` / `admin` (Grafana may prompt you to change the password).

In Grafana:
1. Connections → Data sources → Add data source → Prometheus.
2. Set URL to `http://host.docker.internal:9090`.
3. Save & test.
4. Create a dashboard panel and query `requests_total`.

Grafana and Prometheus are separate containers. The Prometheus container must be running for Grafana to query it.

## Postman requests
- POST `http://127.0.0.1:8000/1?v=hello`
- GET `http://127.0.0.1:8000/`
- PUT `http://127.0.0.1:8000/1?v=updated`
- DELETE `http://127.0.0.1:8000/1`

## Git and GitHub
Replace the URL with your repository:
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

Feature branch:
```powershell
git checkout -b feature/update-crud
git add .
git commit -m "Update CRUD application"
git push -u origin feature/update-crud
```
Create and merge the pull request on GitHub. Then:
```powershell
git checkout main
git pull origin main
```

## Terraform
```powershell
terraform init
terraform plan
terraform apply
```
Type `yes` when prompted. Terraform creates `hello.txt`.

## Important
- Week 5 Docker build/run and Week 7 `deploy.bat` are alternative ways to perform the same initial deployment.
- The provided `deploy.bat` is for a fresh container name. Running it again while `crud-container` exists will fail unless you remove/rename the existing container.
- `prometheus.yml` assumes the FastAPI app is reachable from Docker Desktop at `host.docker.internal:8000`.
- The CI workflow tests and builds the image; it does not deploy it.
- Kubernetes is intentionally excluded.
