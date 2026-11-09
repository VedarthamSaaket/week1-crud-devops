from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_crud():
    assert client.post("/1?v=hello").json() == {"1": "hello"}
    assert client.get("/").json() == {"1": "hello"}
    assert client.put("/1?v=updated").json() == {"1": "updated"}
    assert client.delete("/1").json() == {"deleted": "updated"}
