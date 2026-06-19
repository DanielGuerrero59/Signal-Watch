# TestClient is a fake browser that sends requests without needing the server to be running
from fastapi.testclient import TestClient

# Goes to app folder to main.py and imports our app server variable
from app.main import app

# Creates fake browser pointed at our app
client = TestClient(app)

import pytest



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
    assert check.json() == { 
        "Start Time": "4/6/2026"
    }


@pytest.fixture
def cleanup():
    # before test — nothing needed here
    yield
    # after test — delete files from uploads/
    if os.path.exists("uploads"):
        # list of file names inside directory
        for filename in os.listdir("uploads")
        #deletes every file in directory after test 
        os.remove(f"uploads/{filename}")


    
    


def test_upload_valid_pdf(cleanup): 
    response = client.post("/upload", files={"file": ("test.pdf", b"fake pdf content", "application/pdf")})
    assert response.status_code == 201 
    assert response.json() == {
    "Filename": "test.pdf",
    "Size": 16,
    "Saved_to": "uploads/test.pdf"
    

}


def test_upload_empty_file(): 
    uploaded_empty = client.post("/upload", files = {"file":  ("empty.txt", b"", "text/plain")})
    # 400 means data format is correct, but inside logic is irrational (empty file)
    assert uploaded_empty.status_code == 400 


def test_upload_too_large(): 
    # +1 above our file limit to properly test larger files 
    large_file = client.post("/upload", files = {"file": ("big.pdf", b"x" * (10 * 1024 * 1024 + 1), "application/pdf")})
    assert large_file.status_code == 413


def test_upload_wrong_type(): 
    wrong_extension = client.post("/upload", files = {"file": ("badtype.js", b"random info", "text/javascript")})
    # HTTP 415 for wrong types of data that cannot be supported 
    assert wrong_extension.status_code == 415


def test_upload_valid_other_types(cleanup): 
    extensions = [".txt", ".png", ".jpg"]
    for ext in extensions: 
        valid_extension = client.post("/upload", files={"file": (f"test{ext}", b"fake jpg content", "image/jpg")})
        assert valid_extension.status_code == 201





