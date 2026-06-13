# TestClient is a fake browser that sends requests without needing the server to be running
from fastapi.testclient import TestClient

# Goes to app folder to main.py and imports our app server variable
from app.main import app

# Creates fake browser pointed at our app
client = TestClient(app)

def test_health_check():
    # Sends a GET request to /health and stores the response
    response = client.get("/health")
    # assert checks if the condition is true — if false, the test fails here
    assert response.status_code == 200
    # Checks the actual JSON body matches exactly what we expect
    assert response.json() == {"status": "ok"}


def test_about_check():
    info = client.get("/about")
    assert info.status_code == 200
    assert info.json() == {
        "project": "SignalWatch",
        "version": "1",
        "description": "Ingests media to human insight"
    }


def test_status():
    check = client.get("/status")
    assert check.status_code == 200


def test_upload_valid():
    # Sends a POST with valid JSON — tests that a well-formed request gets accepted
    checkStatus = client.post("/upload", json={
        "filename": "TestFile",
        "size": 20,
        "description": "ValidFileDesc"
    })
    assert checkStatus.status_code == 201


def test_upload_invalid():
    # filename should be a string but we're passing an integer (20)
    # Pydantic catches this mismatch and automatically returns 422 Unprocessable Entity
    invalidUpload = client.post("/upload", json={
        "filename": 20,
        "size": 20,
        "description": "ValidFileDesc"
    })
    #422 meaning something within the format of the data itself was incorrect (such as a mismatch)
    assert invalidUpload.status_code == 422



def test_upload_valid_pdf(): 
    response = client.post("/upload", files={"file": ("test.pdf", b"fake pdf content", "application/pdf")})
    assert response.status_code == 201 


def test_upload_empty_file(): 
    uploaded_empty = client.post("/upload", files = {"file":  ("empty.txt", b"", "text/plain")})
    # 400 means data format is correct, but inside logic is irrational (empty file)
    assert uploaded_empty.status_code == 400 







