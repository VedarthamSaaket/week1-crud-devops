import logging

from fastapi import FastAPI
from prometheus_client import Counter, make_asgi_app

logging.basicConfig(level=logging.INFO)
requests = Counter("requests_total", "Total requests")

app = FastAPI()
app.mount("/metrics", make_asgi_app())

data = {}


@app.middleware("http")
async def monitor(request, call_next):
    response = await call_next(request)
    requests.inc()
    logging.info(
        "%s %s %s",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


@app.post("/{i}")
def create(i: int, v: str):
    data[i] = v
    return data


@app.get("/")
def read():
    return data


@app.put("/{i}")
def update(i: int, v: str):
    data[i] = v
    return data


@app.delete("/{i}")
def delete(i: int):
    return {"deleted": data.pop(i, None)}
